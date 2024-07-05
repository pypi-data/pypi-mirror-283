from scp import SCPClient
import paramiko
import sys
import os
import subprocess
import select
import socket
import logging
import termios
import tty
import pivotr.nodes.node_funcs as node_funcs
import pivotr.networking.networking_funcs as networking_funcs

# Establish a tunnel between pivotr and final host in ip_chain list, returns final host client
def build_ssh_tunnel(ip_chain, pnodes):

    # Establish channels between nodes recursively
    def build_tunnel(c, addr, hosts, counter):

        if (addr == ip_chain[-1]):
            return c, hosts, counter

        # Build tunnel between previous node and next node in ip_chain list
        if (counter == 0):
            prev_node = (pnodes[0].addr, 22)
        else:
            prev_node = (ip_chain[counter - 1], 22)
        next_node = (ip_chain[counter + 1], 22)

        c_transport = c.get_transport()
        c_channel = c_transport.open_channel("direct-tcpip", next_node, prev_node)

        node = node_funcs.get_node_by_addr(ip_chain[counter + 1], pnodes)

        if not node.node_owned():
            node.get_creds()
        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            if node.ssh_keyfile:
                pkey = paramiko.RSAKey.from_private_key_file(node.ssh_keyfile)
                #client.connect(next_node[0], username=node.username, key_filename=node.ssh_keyfile, sock=c_channel)
                client.connect(next_node[0], username=node.username, pkey=pkey, sock=c_channel)
            else:
                client.connect(next_node[0], username=node.username, password=node.passwd, sock=c_channel)

            #client.connect(next_node, username=node.username, password=node.passwd, sock=c_channel)

        except paramiko.ssh_exception.AuthenticationException:
            print('Authentication failed at node n' + str(node.node_id))
            sys.exit(2)

        hosts.append(client)

        counter += 1
        client, hosts, counter = build_tunnel(client, ip_chain[counter], hosts, counter)
        return client, hosts, counter

    # Setup a logger to announce only critical errors with SSH connection (prevents spam from ping_sweep)
    logging.basicConfig()
    logging.getLogger("paramiko").setLevel(logging.CRITICAL)
    counter = 0
    hosts   = []
    node    = node_funcs.get_node_by_addr(ip_chain[counter], pnodes)

    # Build our client object based on creds from node, current chain address and next address
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        if node.ssh_keyfile:
            client.connect(ip_chain[counter], username=node.username, key_filename=node.ssh_keyfile)
        else:
            client.connect(ip_chain[counter], username=node.username, password=node.passwd)
    except paramiko.ssh_exception.AuthenticationException:
        print('Authentication failed at node n' + str(node.node_id))
        sys.exit(2)
    except:
        print('[-] Unable to establish SSH connection')
        sys.exit(2)

    if (len(ip_chain) == 1):
        return client, hosts

    client, hosts, counter = build_tunnel(client, ip_chain[counter], hosts, counter)
    return client, hosts

# Begin SSH server, used for sending commands, interactive sessions, and using SCP for file transfers
def ssh_server(node):
    client = paramiko.SSHClient()

    # client can also support using key files
    # client.load_host_keys('/home/user/.ssh/known_hosts')

    # Establish a connection to target server
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

    try:
        client.connect(node.addr, username=node.username, password=node.passwd)
    except paramiko.ssh_exception.AuthenticationException:
        print('Authentication failed at node n' + str(node.node_id))
        sys.exit(2)
    except:
        print('[-] Unable to establish SSH connection')
        sys.exit(2)

    return client

def scp_get(node, pnodes, filename):

    ip_chain = networking_funcs.build_ip_chain(node, pnodes)

    client, hosts_to_close = build_ssh_tunnel(ip_chain, pnodes)
    scp = SCPClient(client.get_transport())
    scp.get(r'' + filename, r'./')

    # Close all connections made in our 'ssh chain'
    for session in reversed(hosts_to_close):
        session.close()

def scp_put(node, pnodes, filename):

    ip_chain = networking_funcs.build_ip_chain(node, pnodes)

    client, hosts_to_close = build_ssh_tunnel(ip_chain, pnodes)
    scp = SCPClient(client.get_transport())
    scp.put(filename, recursive=True, remote_path='/tmp')

    # Close all connections made in our 'ssh chain'
    for session in reversed(hosts_to_close):
        session.close()

def ssh_command(node, pnodes, command):

    ip_chain = networking_funcs.build_ip_chain(node, pnodes)
    client, hosts_to_close = build_ssh_tunnel(ip_chain, pnodes)

    stdin, stdout, stderr = client.exec_command(command)
    output = (stdout.read().decode('utf-8'))
    print(output)

    # Close all connections made in our 'ssh chain'
    for session in reversed(hosts_to_close):
        session.close()
    return output

# Establish a live SSH connection to last host in ip_chain list
def ssh_interactive(node, pnodes):

    # Shell function
    def open_shell(connection):

        oldtty_attrs = termios.tcgetattr(sys.stdin)

        # invoke_shell with default options is vt100 compatible
        # which is exactly what you want for an OpenSSH imitation
        channel = connection.invoke_shell()

        def resize_pty():
            # resize to match terminal size
            tty_height, tty_width = \
                    subprocess.check_output(['stty', 'size']).split()

            # try to resize, and catch it if we fail due to a closed connection
            try:
                channel.resize_pty(width=int(tty_width), height=int(tty_height))
            except paramiko.ssh_exception.SSHException:
                pass

        try:
            stdin_fileno = sys.stdin.fileno()
            tty.setraw(stdin_fileno)
            tty.setcbreak(stdin_fileno)

            channel.settimeout(0.0)

            is_alive = True

            while is_alive:
                # resize on every iteration of the main loop
                resize_pty()

                read_ready, write_ready, exception_list = \
                        select.select([channel, sys.stdin], [], [])

                # if the channel is one of the ready objects, print
                # it out 1024 chars at a time
                if channel in read_ready:
                    # try to do a read from the remote end and print to screen
                    try:
                        out = channel.recv(1024).decode('utf-8')

                        # remote close
                        if len(out) == 0:
                            is_alive = False
                        else:
                            # rely on 'print' to correctly handle encoding
                            print(out, end='')
                            sys.stdout.flush()

                    # do nothing on a timeout, as this is an ordinary condition
                    except socket.timeout:
                        pass

                # if stdin is ready for reading
                if sys.stdin in read_ready and is_alive:

                    char = os.read(stdin_fileno, 1)

                    # if this side of the connection closes, shut down gracefully
                    if len(char) == 0:
                        is_alive = False
                    else:
                        channel.send(char)

            channel.shutdown(2)

        finally:
            termios.tcsetattr(sys.stdin, termios.TCSAFLUSH, oldtty_attrs)
            print('[+] SSH connection closed.')

    ip_chain = networking_funcs.build_ip_chain(node, pnodes)

    # Build an SSH tunnel from end to end of the ip_chain
    client, hosts_to_close = build_ssh_tunnel(ip_chain, pnodes)
    
    open_shell(client)
    client.close()

    # Close all connections made in our 'ssh chain'
    for session in reversed(hosts_to_close):
        session.close()
