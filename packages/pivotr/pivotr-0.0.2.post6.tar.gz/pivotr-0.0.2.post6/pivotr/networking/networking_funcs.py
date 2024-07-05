import re
import subprocess
import netifaces
import ipaddress
import concurrent.futures
import pivotr.nodes.nodes as nodes
import pivotr.nodes.node_funcs as node_funcs
import pivotr.networking.ssh_funcs as ssh_funcs

# Build chain of hosts from server to node
def build_ip_chain(node, pnodes):
    ip_chain = []

    # Build chain
    def build_list(node, pnodes, ip_chain):

        # Append current node address to beginning of ip_chain list to maintain proper order of execution
        ip_chain.insert(0, node.addr)
        
        # If the parent node of the current node is node_id 0 (server) then return our chained list of addresses
        if node.parent_node.node_id == 0:
            return ip_chain
        else:
            # Otherwise add current node's address and run this function recursively
            build_list(node.parent_node, pnodes, ip_chain)
            return ip_chain

    # Run our recursive building function and return the final list
    ip_chain = build_list(node, pnodes, ip_chain)
    return ip_chain

# Return ip and cidr info
def get_network_info():

    # Get interfaces, then IP from default interface
    ifaces = netifaces.interfaces()
    ip_addr = ''
    subnet_addr = ''
    cidr = 24
    
    # Iterate through devices
    for iface in ifaces:
        try:
            # Pull IP associated with each device, use non-loopback IP
            ip_addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["addr"]
            if ip_addr != '127.0.0.1':

                # Calculate subnet mask and derive CIDR from mask
                subnet_addr = netifaces.ifaddresses(iface)[netifaces.AF_INET][0]["netmask"]
                cidr = sum(bin(int(x)).count('1') for x in subnet_addr.split('.'))
        except:
            pass

    return ip_addr, cidr

# Return all valid IPs of last node in ip_chain list (useful for multi-home hosts)
def get_all_addrs(node, pnodes):

    # Get list of nodes to pivot through
    ip_chain = build_ip_chain(node, pnodes)

    # Establish our SSH tunnel to the last node in the chain
    client, hosts_to_close = ssh_funcs.build_ssh_tunnel(ip_chain, pnodes)

    try:
        # Run 'ip addr' on last host in ip_chain list and capture output
        stdin, stdout, stderr = client.exec_command('ip addr')
        output = (stdout.read().decode('utf-8'))
    except:
        pass

    # Strip all valid IP addresses from output
    ip_addrs = re.findall( r'[0-9]+(?:\.[0-9]+){3}+\/[0-9]{1,2}', output)

    # Iterate through list and remove loopback
    candidates = []
    for addr in ip_addrs:
        candidate = addr.strip('inet ')
        if candidate == '127.0.0.1/8':
            continue
        candidates.append(candidate)

     # Close all connections made in our 'ssh chain'
    for session in reversed(hosts_to_close):
        session.close()

    return candidates
    

# Ping sweep from a given node and add discovered hosts to 
def ping_sweep(node, pnodes):
    
    # If pinging pivotr host's subnet, no need to build an SSH tunnel
    if node.node_id == 0:

        # Simple ping function that appends successful pings to active_hosts list
        def ping(ip_addr):
            try:
                subprocess.check_output(["ping", "-c", "1", ip_addr])
                active_hosts.append(ip_addr)
            except:
                pass

        # Obtain node IP and CIDR info
        ip_addr, cidr = get_network_info()

        # Establish network info based on IP/CIDR
        network = ipaddress.ip_network(ip_addr + '/' + str(cidr), strict=False)
        hosts = network.hosts()
        active_hosts = []

        print('[+] Performing host discovery on n' + str(node.node_id) + ' (' + node.addr + ') subnet')

        # Ping sweep with threading and store live hosts in hosts list
        executor = concurrent.futures.ThreadPoolExecutor(254)
        for candidate_addr in hosts:
            executor.submit(ping, str(candidate_addr))

    else:

        # Ping function, modified to go through our SSH tunnel
        def ping(ip_addr, client):
            try:
                stdin, stdout, stderr = client.exec_command('ping -c1 ' + str(ip_addr))
                if (stdout.read()):
                    active_hosts.append(ip_addr)
            except ssh_exception.NoValidConnectionsError:
                print('No connections')

        # Link all nodes between pivotr host and final host in ip_chain list
        ip_chain = build_ip_chain(node, pnodes)
        client, hosts_to_close = ssh_funcs.build_ssh_tunnel(ip_chain, pnodes)

        # Get all ip addresses associated with node (in case it is multi-homed)
        addrs = get_all_addrs(node, pnodes)
        active_hosts = []

        # Establish our node connection
        client, hosts_to_close = ssh_funcs.build_ssh_tunnel(ip_chain, pnodes)

        # Iterate through all IPs associated with node
        for node_ip in addrs:

            print('[+] Performing host discovery on n' + str(node.node_id) + ' (' + node_ip + ') subnet')

            # Build a list of hosts given the IP/CIDR subnet and initialize our list of active hosts
            ip = ipaddress.ip_network(node_ip, strict=False)
            hosts = ip.hosts()
            
            # If subnet of IP is the same as pivotr subnet, skip
            raw_ip = node_ip.rsplit('/')
            if raw_ip[0] == node.addr:
                continue

            executor = concurrent.futures.ThreadPoolExecutor(254)
            for candidate_addr in hosts:
                executor.submit(ping, str(candidate_addr), client)

        # Close all connections made in our 'ssh chain'
        for session in reversed(hosts_to_close):
            session.close()

    # Iterate live hosts list and build nodes for each one
    if len(active_hosts) > 0:
        for h in active_hosts:
            if not node_funcs.verify_node_addr(h, pnodes):
                node_id = int(pnodes[-1].node_id + 1)
                pnodes.append(nodes.Node(node_id, node, h))
                print('[+] Node added: n'+ str(node_id) + ' - ' + h)
    else:
        print('[-] No new hosts discovered.')

