#!/usr/bin/env python
#
##############################################################################################################
# Author: Maturon Miner III
# License: GPLv3
#
# Pivotr - This project aims to establish seemless connectivity between compromised machines on a network
# via SSH tunneling while also providing host discovery tools as well as a CLI-based illustration of all
# known hosts connected, directly or indirectly, to our primary host machine.
#
# Phase 1 - Establish a wholly functional network-based SSH routing infrastructure while supplying tools
# for continued mapping of the network itself and subnets that we contact through compromised nodes. This
# phase relies on credentials being obtained through other means and does NOT actually provide any sort of
# exploitation devices of its own and is functional soley as a convenience for organization of already
# compromised hosts. This phase was more or less completed on 02/01/2024.
#
# Phase 2 - Enact agent executables that, when uploaded and executed on targets, have callback features which
# make reverse-shell connections, maintain persistence, and obfuscate and exfiltrate data to a 'server'
# daemon that is run/modified by the pivotr.py application. Agent features and the data they obtain will
# be integrated into pivotr's current mapping features and data maintenance functionality, and current node
# objects will expand greatly to incorporate the new information available to us through these agents.
#
##############################################################################################################

import os
import sys
import argparse
import pivotr.file.file_funcs as file_funcs
import pivotr.nodes.nodes as nodes
import pivotr.nodes.node_funcs as node_funcs
import pivotr.networking.ssh_funcs as ssh_funcs
import pivotr.networking.networking_funcs as networking_funcs

VERSION = '0.0.2-6'

def usage():
	print('pivotr v'+ VERSION)
	print('Usage: pivotr <ARGS> [OPTIONS]')
	print('')
	print('[ARGS]')
	print('  -n,--node=<NODE_ID>'.ljust(30)  + 'Perform node-related action (no further args prompts to add new node')
	print('  -m,--map'.ljust(30)  + 'Display map of all active nodes')
	print('  -s,--snapshot'.ljust(30)  + 'Save an encrypted snapshot of current node data to snapshots directory')
	print('  -f,--filename'.ljust(30)  + 'Specify a different node data file. Changes take place with next pivotr command')
	print('  -C,--clear'.ljust(30)  + 'Delete all node data')
	print('[NODE OPTIONS]')
	print('  <NO NODE ID>'.ljust(30)  + 'Add a new node')
	print('  <NO FLAG>'.ljust(30)  + 'View all data corresponding to node <NODE_ID>')
	print('  -e,--edit'.ljust(30)  + 'Modify node <NODE_ID>')
	print('  -D,--delete'.ljust(30)  + 'Delete node <NODE_ID>')
	print('  -c,--command=<COMMAND>'.ljust(30)  + 'Run command <COMMAND> from node <NODE_ID>')
	print('  -i,--interactive'.ljust(30)  + 'Open SSH connection on node <NODE_ID>')
	print('  -u,--upload'.ljust(30)  + 'Upload file <FILE> to /tmp directory of node <NODE_ID>')
	print('  -d,--download'.ljust(30)  + 'Download file <FILE> from node <NODE_ID>')
	print('  -S,--scan'.ljust(30)  + 'Ping sweep subnet of node <NODE_ID> and add all discoveries to nodes list')
	#print('  -P,--port-forward'.ljust(30) + 'Port forward <PARENT_NODE_ID>:<PORT> --> <CHILD_NODE_ID>:<PORT>')
	print('[MISC OPTIONS]')
	#print( '  -d,--device=<DEVICE>'.ljust(30)  + 'Specify networking device <DEVICE>')
	print('  -p,--port=<PORT>'.ljust(30)  + 'Specify port <PORT> for any commands that utilize a port')
	print('  -v,--version'.ljust(30)  + 'Print version and exit')
	print('  -h,--help'.ljust(30)  + 'Print help and exit')
	print('')
	print('[EXAMPLES]')
	print('  pivotr -n'.ljust(40) + 'Add a new node')
	print('  pivotr -n9'.ljust(40) + 'View all data corresponding to node #9')
	print('  pivotr -n7 -D'.ljust(40) + 'Delete node #7 and any of its subsequent child nodes')
	print('  pivotr -n1 -c \'ping 10.10.11.120\''.ljust(40) + 'Run \'ping 10.10.11.120\' from node #1')
	print('  pivotr -n2 -i'.ljust(40) + 'Open an interactive SSH session on node #2')
	print('  pivotr -C'.ljust(40) + 'Delete all nodes')
	sys.exit()

def main():

	# Vars
	server_addr, cidr 	= networking_funcs.get_network_info()
	port 				= 6666
	pnodes 				= []
	config_dir			= os.path.expanduser("~") + '/.config/pivotr'
	data_file 			= config_dir + '/nodes.data'
	key_file 			= config_dir + '/pivotr.key'

	# If we don't have a '~/.config/pivotr' directory, make it (in order to store config file and data)
	try:
		os.mkdir(config_dir)
	except:
		pass

	# Generate a key for encrypting/decrypting our data file and store in the root pivotr directory. Set restrictive permissions
	if (not os.path.exists(key_file)):
		print('No key file found. Generating pivotr.key for data encryption/decryption.')
		file_funcs.generate_key(key_file)
		os.chmod(key_file, 0o600)

	# Initialize our key variable for use
	key = file_funcs.get_key(key_file)

	# Setup command line args
	parser = argparse.ArgumentParser(description='Pivotr - A remote command execution framework', add_help=False)
	group1 = parser.add_mutually_exclusive_group()
	group2 = parser.add_mutually_exclusive_group()
	parser.add_argument('--port', '-p', type=int, nargs='*')
	group1.add_argument('--filename', '-f', nargs='*')
	group1.add_argument('--help', '-h', action='store_true')
	group1.add_argument('--node', '-n', nargs='*')
	group1.add_argument('--add', '-a', action='store_true')
	group1.add_argument('--map', '-m', action='store_true')
	group1.add_argument('--clear', '-C', action='store_true')
	group1.add_argument('--snapshot', '-s', action='store_true')
	group1.add_argument('--version', '-v', action='store_true')
	group2.add_argument('--command', '-c', nargs='*')
	group2.add_argument('--interactive', '-i', action='store_true')
	group2.add_argument('--edit', '-e', action='store_true')
	group2.add_argument('--delete', '-D', action='store_true')
	group2.add_argument('--upload', '-u', nargs='*')
	group2.add_argument('--download', '-d', nargs='*')
	#group2.add_argument('--port-forward', '-P', nargs='*')
	group2.add_argument('--scan', '-S', action='store_true')

	parser.add_argument('--test', '-t', action='store_true')

	# Parse command line args
	args = parser.parse_args()

	# If there is no data file or it has no data, create it and add our server. Otherwise, unpickle data and save in pnodes list
	try:
		if (not os.path.exists(data_file) or os.path.getsize(data_file == 0)):
			pnodes.append(nodes.Server_Node(server_addr))
			file_funcs.put_data(pnodes, data_file)
			file_funcs.encrypt_file(data_file, key)
		else:
			pnodes = file_funcs.get_nodes(data_file, key)
	except:
		print('Error creating/editing node data file. Exiting.')
		sys.exit(2)

	# Use port other than default
	if args.port:
		port = args.port[0]

	# Print help and exit
	if args.help:
		usage()

	elif args.version:
		print('pivotr - v' + VERSION)
		sys.exit(0)

	# Copy encrypted node data file to /tmp, decrypt and extract data, then encrypt
	elif args.filename:
		try:
			os.popen('cp ' + args.filename[0] + ' ' + data_file)
			print('Now using ' + args.filename[0] + ' for future pivotr data.')
			print('Effects will take place after this command.')
		except:
			print('Error opening ' + data_file)
			sys.exit(2)

	# Save our current nodes data to snapshots directory
	elif args.snapshot:
		file_funcs.save_data(data_file)

	# Map out all current nodes
	elif args.map:
		node_funcs.map_nodes(pnodes)

	# Clear all node data (confirm before executing)
	elif args.clear:
		file_funcs.clear_data(data_file)

	# Debugging function
	elif args.test:
		node_funcs.test_nodes(pnodes)

	# If args.node is a list with no values, treat as 'add new node'
	elif type(args.node) is list:
		if len(args.node) == 0:
			pnodes.append(node_funcs.add_node(pnodes))
			file_funcs.update_nodes(pnodes, data_file, key)

		# If list is populated, determine list args and treat accordingly
		else:

			# Convert node_id arg to object
			n = node_funcs.get_node_by_id(int(args.node[0]), pnodes)

			# Make sure the node exists before doing anything else
			if not n:
				print('n' + str(args.node[0]) + ': node does not exist.')
				sys.exit(2)

			# List of commands to run against our node object
			if args.interactive:
				ssh_funcs.ssh_interactive(n, pnodes)
			elif args.command:
				ssh_funcs.ssh_command(n, pnodes, args.command[0])
			elif args.edit:
				n.edit_node(pnodes)
				file_funcs.update_nodes(pnodes, data_file, key)
			elif args.delete:
				pnodes = node_funcs.delete_node(n, pnodes)
				file_funcs.update_nodes(pnodes, data_file, key)
			elif args.upload:
				ssh_funcs.scp_put(n, pnodes, args.upload[0])
			elif args.download:
				ssh_funcs.scp_get(n, pnodes, args.download[0])
			elif args.scan:
				networking_funcs.ping_sweep(n, pnodes)
				file_funcs.update_nodes(pnodes, data_file, key)
			else:
				n.view_node()
	else:
		usage()