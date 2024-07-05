from getpass import getpass
import os

class Server_Node:
	def __init__(self, addr, node_id=0):
		self.node_id 	= node_id 			# Server node ID, defaults to '0'
		self.addr 		= addr 				# Ip address that the node resides on
		self.childNodes	= []				# List of child nodes that belong to this node

	def view_node(self):
		print('Node ID:   ' + str(self.node_id))
		print('IP addr:   ' + self.addr)

class Node:
	def __init__(self, node_id, parent_node, addr):
		self.node_id 		= node_id
		parent_node.childNodes.append(self)		# Append this node to another node's childNodes list
		self.parent_node 	= parent_node 		# Store parent node
		self.addr 			= addr
		self.username 		= '' 				# Default username from creds{}
		self.passwd 		= '' 				# Corresponding default password from creds{}
		self.ssh_keyfile	= ''				# Private key location (if any)
		self.creds 			= {}				# Stores creds as {'username':['password', 'private_key_location']}
		self.childNodes		= []				# List of child nodes that belong to this node

	# View node attributes
	def view_node(self):
		print('╭─────────────────╮')
		print('│ n' + str(self.node_id).ljust(15) + '│')
		print('│' + self.addr.center(17) + '│')
		print('╰───┬─────────────╯')
		print('    │ Attributes:')
		print('    ╰─┬─Node ID:        ' + str(self.node_id))
		print('      ├─Parent ID:      ' + str(self.parent_node.node_id))
		print('      ├─IP address:     ' + self.addr)
		print('      ├─Child nodes:')

		# Iterate through all child nodes and print them accordingly
		for child in self.childNodes:
			if len(self.childNodes) == 0:
				print('      │    ╰─n/a')
				break
			if child == self.childNodes[-1]:
				print('      │    ╰─n' + str(child.node_id) + ' - [' + child.addr + ']')
			else:
				print('      │    ├─n' + str(child.node_id) + ' - [' + child.addr + ']')

		print('      ╰─Credentials:')
		
		# Iterate through our credentials and print them accordingly
		if not self.creds.keys():
			print('           ╰─n/a')
		else:
			for un, pw in self.creds.items():

				# Append a (default) tag to the credentials currently in use for this node
				if un == self.username:
					display_name = un + ' (default)'
				else:
					display_name = un
				if un == list(self.creds.keys())[-1]:
					print('           ╰─' + display_name)
				else:
					print('           ├─' + display_name)
		#print('DEBUG - creds list: ' + str(self.creds))

	# Modify values of node
	def edit_node(self, pnodes):

		# Print a 'banner' for the node we're working on
		print('╭─────────────────╮')
		print('│ n' + str(self.node_id).ljust(15) + '│')
		print('│' + self.addr.center(17) + '│')
		print('╰───┬─────────────╯')

		while True:
			print('    │ Edit:')
			print('    ╰─┬─(a)ddress')
			print('      ├─(c)redentials')
			print('      ╰─(e)xit')
			print('')
			choice = input("Selection: ")
			match choice:

				# Modify the node's IP address (may make self.addr a list eventually to differentiate multi-homed hosts)
				case 'a' | 'A':
					self.addr = input("New node address: ")

				# Enter our credential-editing cases
				case 'c' | 'C':
					while True:

						# If we don't have credentials, run self.get_creds() to add new ones
						if not self.creds.keys():
							print('No credentials listed for this node.')
							self.get_creds()
							break
						count = 1
						name_to_edit = ''
						print('    │ Credentials:')

						# Iterate through node credentials and display them
						for username, passwd in self.creds.items():
							if username == self.username:
								display_name = username + ' (default)'
							else:
								display_name = username
							if count == 1:
								print('    ╰─┬─(' + str(count) + ') ' + display_name)
							else:
								print('      ├─(' + str(count) + ') ' + display_name)
							count += 1
						print('      ├─(a)dd credentials')
						print('      ╰─(b)ack')
						print('')

						choice = input('Selection: ')
						if choice == 'a' or choice == 'A':
							self.get_creds()
							break
						if choice == 'b' or choice == 'B':
							break
						count = 1

						# Iterate through node credentials again to match user choice to credentials picked
						for username, passwd in self.creds.items():
							if int(choice) == count:
								name_to_edit = username
								#pw_to_edit = passwd
								break
							count += 1

						# Give modification options for credentials
						print('    │ Modify credentials:')
						print('    ╰─┬─(m)ake default')
						print('      ├─(e)dit password')
						print('      ├─(a)dd private key')
						print('      ├─(d)elete')
						print('      ╰─(b)ack')
						print('')

						choice = input('Selection: ')
						match choice:

							# Reassign our username and passwd default values
							case 'm' | 'M':
								self.username = name_to_edit
								self.passwd = self.creds[name_to_edit][0]
								break

							# Get new UN/PW, create the new key, delete the old key, and apply new password to new key
							case 'e' | 'E':
								self.creds[name_to_edit][0] = getpass('New password: ')
								if (name_to_edit == self.username):
									self.passwd = self.creds[name_to_edit][0]
								break

							# Specify private key location (in case of keyfile login)
							case 'a' | 'A':
								self.creds[name_to_edit][1] = input("Private key location: ")
								if (name_to_edit == self.username):
									self.ssh_keyfile = self.creds[name_to_edit][1]
								break

							# Delete the set of credentials entirely
							case 'd' | 'D':
								del self.creds[name_to_edit]
								break
							case 'b' | 'B':
								break

				case 'e' | 'E':
					break
				case _:
					print('Invalid choice')
					continue
		print('[+] Node n' + str(self.node_id) + ' successfully updated.')

	# Store new credentials for a node
	def get_creds(self):
		print('Adding credentials to n' + str(self.node_id) + ' - ' + str(self.addr) + ':')
		new_username = input("New username: ")
		new_passwd = getpass("New password: ")
		self.creds[new_username] = [new_passwd, '']

		# Give option to make these credentials the default for this node
		default = input('Make this the default login for this node? (Y/n): ')
		if (default == 'y' or default == 'Y'):
			self.username = new_username
			self.passwd = new_passwd
			print('Setting to default')
		else:
			print('Default credentials remain unchanged')

	"""
	# Return selected credentials to use for a node
	def use_creds(self):

		# No need to list anything or request input if only one set of credentials exists. Simply return the un/pw
		if len(self.creds.items()) == 1:
			username = list(self.creds.keys())[0]
			passwd = list(self.creds.values())[0]
			return username, passwd

		# If we have multiple login credentials, have user choose which set to use and return the un/pw
		while True:
			count = 1
			print('Credentials for n' + str(self.node_id) + ' - ' + str(self.addr) + ':')
			for username, passwd in self.creds.items():
				print(str(count) + ') ' + username)
				count += 1
			choice = int(input('Number to use: '))
			if choice < 1 or choice > count:
				print('Invalid input')
				continue
			count = 1
			for username, passwd in self.creds.items():
				if choice == count:
					return username, passwd
				count += 1
	"""

	# Return True if we have credentials for the object addr and False otherwise
	def node_owned(self):
		if self.creds.keys():
			for username, passwd in self.creds.items():
				if username:
					if passwd[0] or passwd[1]:
						return True
		return False