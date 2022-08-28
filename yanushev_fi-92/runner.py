import re
from rd_tree import RDTree


collections = {}
tree = RDTree()


def col_exist(collection_name):
    if collection_name not in collections.keys():
        print('!!! THERE IS NO SUCH COLLECTION !!!')
        return False
    return True


def print_tree(collection_name: str):
    if not col_exist(collection_name):
        return
    print(f'{collection_name} tree:')
    root = collections[collection_name]
    dct = RDTree().convert_tree_to_dict(root)
    RDTree().print_dependency_tree(dct, str(root.value))
    print(' ')


def create_collection(collection_name):
    if collection_name in collections.keys():
        print('This collection already created')
        return
    collections[collection_name] = None
    print(f'Created collection {collection_name}')


def insert_data(data, collection_name):
    if not col_exist(collection_name):
        return
    root = collections[collection_name]
    collections[collection_name] = RDTree().insert(root, set(data))


def get_leaves(collection_name: str):
    root = collections[collection_name]
    return RDTree().get_leaf_nodes(root)


def search(collection_name: str, options=None, data=None):
    if not col_exist(collection_name):
        return
    if not options:
        for leaf in get_leaves(collection_name):
            print(leaf)
    root = collections[collection_name]
    if options == 'intersects':
        inter = RDTree().search_intersects(root, set(data))
        for res in inter:
            print(res)
    if options == 'contains':
        cont = RDTree().search_contains(root, set(data))
        for res in cont:
            print(res)
    if options == 'contained_by':
        cont_by = RDTree().search_contained_by(root, set(data))
        for res in cont_by:
            print(res)


def contains(collection_name: str, data: list):
    if not col_exist(collection_name):
        return
    root = collections[collection_name]
    conts = RDTree().contains(root, set(data))
    print(conts)


patterns = {
    'create': r' *create +[a-zA-Z0-9]+ *',
    'search': r' *search +[a-zA-Z0-9]+ *',
    'search_where': r' *search +[a-zA-Z0-9]+ +where +(intersects|contains|contained_by) +{[ 0-9,]+} *',
    'contains': r' *contains +[a-zA-Z0-9]+ +{[ 0-9,]+} *',
    'insert': r' *insert +[a-zA-Z0-9]+ +{[ 0-9,]+} *',
    'exit': r' *exit *',
    'print': r' *print_tree +[a-zA-Z0-9]+ *'
}


def start_query():
    query = ''
    while not query.endswith(';'):
        query = query + ' ' + input('>').strip()
    for command in query.split(';'):
        if command:
            com = if_there_command(command)
            if com[0]:
                if com[1] == 'exit':
                    quit()
                if com[1] == 'print':
                    print_tree(command.split()[1])
                if com[1] == 'create':
                    arg = get_create(command)
                    create_collection(collection_name=arg)
                if com[1] == 'search':
                    args = get_search(command, where=False)
                    search(args)
                if com[1] == 'search_where':
                    args = get_search(command, where=True)
                    search(args[0], args[1], args[2])
                if com[1] == 'contains':
                    args = get_contains(command)
                    contains(args[1], args[0])
                if com[1] == 'insert':
                    args = get_insert(command)
                    insert_data(args[0], args[1])
            else:
                print(com[1])
    start_query()


def if_there_command(command):
    for key, value in patterns.items():
        if bool(re.fullmatch(value, command)):
            return True, key
    msg = 'Error! There no such command or there is a mistake in an existing one!'
    return False, msg


def clean_command(command):
    return re.sub(r' +', ' ', command).strip()


def get_create(command):
    com_cln = clean_command(command)
    return com_cln.split()[1]


def get_insert(command):
    com_clean = clean_command(command)
    splitted = re.split(r'{| |,|}', re.findall(r'{.*}', com_clean)[0])
    return [int(x) for x in splitted if x], com_clean.split()[1]


def get_contains(command):
    com_clean = clean_command(command)
    splitted = re.split(r'{| |,|}', re.findall(r'{.*}', com_clean)[0])
    return [int(x) for x in splitted if x], com_clean.split()[1]


def get_search(command, where=True):
    com_cln = clean_command(command)
    splt = com_cln.split()
    if where:
        splitted = re.split(r'{| |,|}', re.findall(r'{.*}', com_cln)[0])
        return splt[1], splt[3], [int(x) for x in splitted if x]
    return splt[1]


if __name__ == '__main__':
    start_query()
