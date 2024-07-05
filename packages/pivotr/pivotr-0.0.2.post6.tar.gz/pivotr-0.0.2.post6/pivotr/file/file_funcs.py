import os
import datetime
import pickle
from cryptography.fernet import Fernet

def update_nodes(nodes, filename, key):
	decrypt_file(filename, key)
	put_data(nodes, filename)
	encrypt_file(filename, key)

def get_nodes(filename, key):
	decrypt_file(filename, key)
	nodes = get_data(filename)
	encrypt_file(filename, key)
	return nodes

# Serialize data for preservation (used to preserve our nodes list)
def put_data(obj_list, filename):
	with open(filename, 'wb') as f:
		pickle.dump(obj_list, f)

# Obtain our preserved data (nodes list)
def get_data(filename):
	data = []
	if os.path.exists(filename):
		with open(filename, 'rb') as f:
			if os.path.getsize(filename) > 0:
				data = pickle.load(f)
	return data

# Save a copy of /tmp/nodes.data to ./snapshots
def save_data(filename):
	if os.path.exists(filename):
		now = datetime.datetime.now()
		new_filename = now.strftime("%Y-%m-%d_%H%M%S-nodes.data")
		cp_string = "cp " + filename + " ./snapshots/" + new_filename
		try:
			os.popen(cp_string)
			print('[+] Saved node data to snapshots/' + new_filename)
		except:
			print('[-] An error occured. No file saved.')

# Delete /tmp/nodes.data (or file specified by -f flag)
def clear_data(filename):

	# A confirmation before deleting data is always preferred
	confirm = 'n'
	confirm = input('Clear all node data? (y/N): ')
	if confirm == 'y' or confirm == 'y':
		try:
			os.remove(filename)
			print('[+] Node data deleted.')
		except:
			print('[-] Unable to locate ' + filename)
	else:
		print('[-] Node data not deleted.')

# Generate a random encryption key
def generate_key(filename):
	key = Fernet.generate_key()

	# Store our key in the main pivotr directory
	with open(filename, 'wb') as filekey:
		filekey.write(key)

def get_key(filename):
	with open(filename, 'rb') as filekey:
		key = filekey.read()
	return key

# Encrypt the contents of a file using the provided key
def encrypt_file(filename, key):
	cipher_suite = Fernet(key)  # Initialize a Fernet object with the encryption key
	with open(filename, 'rb') as file:
		plaintext = file.read()  # Read the plaintext data from the file
	encrypted_data = cipher_suite.encrypt(plaintext)  # Encrypt the plaintext data
	with open(filename, 'wb') as encrypted_file:
		encrypted_file.write(encrypted_data)  # Overwrite existing encrypted file with new data

# Decrypt the contents of an encrypted file using the provided key
def decrypt_file(filename, key):
	cipher_suite = Fernet(key)  # Initialize a Fernet object with the key
	with open(filename, 'rb') as encrypted_file:
		encrypted_data = encrypted_file.read()  # Read the encrypted data from the file
	decrypted_data = cipher_suite.decrypt(encrypted_data)  # Decrypt the data
	with open(filename, 'wb') as decrypted_file:
		decrypted_file.write(decrypted_data)  # Write the decrypted data