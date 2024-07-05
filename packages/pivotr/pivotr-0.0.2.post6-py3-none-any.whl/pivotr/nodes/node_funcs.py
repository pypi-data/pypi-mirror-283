import pivotr.nodes.nodes as nodes
from getpass import getpass

# Get new node info and return new node object
def add_node(pnodes):
    verify_pid  = False                     # parent ID flag
    verify_addr = False                     # IP addr flag
    node_id     = int                       # Initialize node ID as integer
    node_id     = pnodes[-1].node_id + 1    # Node ID is the highest current node ID + 1

    print('[+] Adding node: n' + str(node_id))

    # Verify the node id exists
    while True:
        parent_id = input('Parent node ID: ')
        
        try:
            for node in pnodes:
                if int(parent_id) == node.node_id:
                    verify_pid = True
                    break
            if verify_pid:
                parent_node = get_node_by_id(int(parent_id), pnodes)
                break
            else:
                print('Unable to locate parent node', parent_id)
        except:
            print('Invalid node id:', parent_id)
            
    # Verify address does NOT already exist
    while True:
        addr = input('Node IP address: ')
        verify_addr = True

        for node in pnodes:
            if addr == node.addr:
                print('Host address ' + str(addr) + ' is current associated with another node.')
                verify_addr = False
                break
        if verify_addr: break

    #username    = input('SSH username: ')
    #passwd      = getpass('SSH password: ')

    return nodes.Node(node_id, parent_node, addr)

# Delete node from nodes list
def delete_node(node, pnodes):

    # Confirm node delete before proceeding
    confirm = 'n'

    try:
        confirm = input('Delete node ' + str(node.node_id) + ' and all attached nodes? (y/N): ')
        if confirm == 'y' or confirm == 'Y':

            # Build list of nodes to delete (select node and all subseqent child nodes)
            def build_child_list(node, delete_list):

                # Iterate through childNodes list if any children exist
                if len(node.childNodes) > 0:
                    for child in node.childNodes:

                        # Run build_child_list recursively on next set of children
                        delete_list = build_child_list(child, delete_list)
                        delete_list.append(child)
                else:

                    # Nodes without children are directly appended to delete list
                    delete_list.append(node)
                    return delete_list

                # After all children are added, add current node and return list
                return delete_list

            # Initialize list, generate list, add primary node to list, remove any repeats, and sort in descending order
            delete_list = []
            delete_list = build_child_list(node, delete_list)
            delete_list.append(node)
            delete_list = list(set(delete_list))
            delete_list.sort(key=lambda x: x.node_id, reverse=True)

            # Get parent node and grandparent node objects
            parent = node.parent_node

            # Delete node from parent's childNodes list
            parent.childNodes.remove(node)

            # Iterate through delete_list and delete all items from pnodes
            for n in delete_list:
                print('[+] Deleting node: n' + str(n.node_id))
                pnodes.remove(n)
    except:
        print('No nodes deleted.')

    # Return nodes for updating
    return pnodes

# Verify if we have access to a node (checks for UN/PW in object only, not via connection)
def verify_node_addr(addr, pnodes):
    for node in pnodes:
        if node.addr == addr:
            return True
    return False

# Return node object based on address
def get_node_by_addr(addr, pnodes):
    for n in pnodes:
        if n.addr == addr:
            return n
    return False

# Return object of node ID or 'False' (which should trigger exception in pivotr.py)
def get_node_by_id(node_id, pnodes):
    for n in pnodes:
        if node_id == n.node_id:
            return n
    return False

def test_nodes(pnodes):
    # Test values (with simplified classes)

    counter = int
    counter = 0
    for node in pnodes:
        print(str(counter) + ':', node.node_id, '- ' + node.addr)
        if (len(node.childNodes) > 0):
            for child in node.childNodes:
                print('   ', child.node_id, '-', child.addr)
        counter += 1

# Map out known nodes
def map_nodes(n):

    # Function for printing all nodes in a nodes childNodes list, aka a nodes "column"
    def print_children(node, pnodes, column, indent_string):
        column += 1

        children = node.childNodes
        
        # Build a string that both indents each node and addes appropriate 'connector' branches when necessary
        # Each iteration through print_children() simply adds to the string what's appropriate for the current childNodes list
        # The string state is stored prior to each subsequent recursive call to print_children() so that the function will print
        # the appopriate string once it is returned to upon exiting recursion
        
        # All first gen nodes (nodes directly connected to our pivotr host) only need an indent, no branches
        if children[0].parent_node.node_id == 0:
            indent_string +=  ('           ')
        else:

            # Get parent node and grandparent node objects
            parent = children[0].parent_node
            grandparent = parent.parent_node
        
            # If the parent is not the LAST node of the grandparent's childNodes list then append a '│'
            if not parent == grandparent.childNodes[-1]:
                indent_string +=  ('│           ')

            # Otherwise just extend the indent by one
            else:
                indent_string +=  ('            ')

        # Store this string so that when recursion ends, we'll use this string for the current function instead of the latest string iteration
        stored_string = indent_string

        # Iterate through all of the current node's children
        for child in node.childNodes:

            # If we're printing the last node in a childNode list, give it a bend instead of branching downward
            if child == node.childNodes[-1]:
                print_owned_node(child, 'bend', indent_string)

            # Otherwise, tee it off so the node below connects
            else:
                print_owned_node(child, 'fork', indent_string)

            if (len(child.childNodes) > 0):
                print_children(child, pnodes, column, indent_string)

                # Restore the indent string to its previous state after exiting recursion
                indent_string = stored_string

        column -= 1

    # Function for printing individual node
    def print_owned_node(obj_node, connection, indent_string):

        # If we have creds for the node, print boxes with solid lines
        if obj_node.node_owned():

            # Every line printed for each box type gets an indent string calculated from print_children()
            print(indent_string + '│  ╭─────────────────╮')

            # If this node is not the last in its childNodes list, print a 'fork' connector
            if (connection == 'fork'):
                print(indent_string + '├──┤ n' + str(obj_node.node_id).ljust(15) + '│')
                print(indent_string + '│  │' + obj_node.addr.center(17) + '│')

                # If this node has children, print a 'connector' branch from the bottom of the box
                if (len(obj_node.childNodes) > 0):
                    print(indent_string + '│  ╰────────┬────────╯')
                else:
                    print(indent_string + '│  ╰─────────────────╯')

            # If this node is the last in its childNodes list, print a 'bend' connector
            elif (connection == 'bend'):
                print(indent_string + '╰──┤ n' + str(obj_node.node_id).ljust(15) + '│')
                print(indent_string + '   │' + obj_node.addr.center(17) + '│')
                if (len(obj_node.childNodes) > 0):
                    print(indent_string + '   ╰────────┬────────╯')
                else:
                    print(indent_string + '   ╰─────────────────╯')

        # No creds for node: print dotted line boxes (don't need bottom branch since they won't have children until we get creds)
        else:
            print(indent_string + '│  ╭ ─ ─ ─ ─ ─ ─ ─ ─ ╮')
            if (connection == 'fork'):
                print(indent_string + '├──┤ n' + str(obj_node.node_id).ljust(15) + '╎')
                print(indent_string + '│  ╎' + obj_node.addr.center(17) + '╎')
                print(indent_string + '│  ╰ ─ ─ ─ ─ ─ ─ ─ ─ ╯')
            elif (connection == 'bend'):
                print(indent_string + '╰──┤ n' + str(obj_node.node_id).ljust(15) + '╎')
                print(indent_string + '   ╎' + obj_node.addr.center(17) + '╎')
                print(indent_string + '   ╰ ─ ─ ─ ─ ─ ─ ─ ─ ╯')

    # Print server node first
    print('╭─────────────────╮')
    print('│' + 'n0 - pivotr'.ljust(17) + '│')
    print('│' + n[0].addr.center(17) + '│')
    print('╰──────────┬──────╯')

    column = 0
    indent_string = ''
    
    try:
        print_children(n[0], n, column, indent_string)
    except:
        print('No further data.')
        print('Try adding a node manually (-a) or performing host discovery (-S)')