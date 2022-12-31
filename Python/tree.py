import json
import collections
import copy
import nested_lookup

def deep_update(source, overrides):
    """
    Update a nested dictionary or similar mapping.
    Modify ``source`` in place.
    """
    for key, value in overrides.iteritems():
        if isinstance(value, collections.Mapping) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source

def update(d, u):
    for k, v in u.items():
        if isinstance(v, collections.abc.Mapping):
            d[k] = update(d.get(k, {}), v)
        else:
            d[k] = v
    return d

def create_tree_from_animals():
    
    f = open('myfile6.json')
    database = json.load(f)
    
    database = database['1']
    
    tree_list = []

    document = [ { 'taco' : 42 } , { 'salsa' : [ { 'burrito' : { 'taco' : 69 } } ] } ]
    print(nested_lookup.nested_lookup('salsa', document))

    exit(0)
    for animal in database['animals']:
        
        print(animal['taxon'])
        
        if animal['taxon'] == 'kingdom':
            print(animal['taxon'], animal['name'], animal['_id'])
            exit(0)
        # break
        
        # children = []
        # for child in animal['children']:
        #     children.append(child['name'])
        
        # tree_list.append([animal['name'], children])

    print(tree_list)

    return tree_list

def add_taxon_to_tree(taxon, tree):
    f = open('myfile6.json')
    database = json.load(f)
    database = database['1']['animals']

    for animal in database:
        if animal['taxon'] == taxon:

            document = tree
            print(document)
            # print(tree)
            # print(animal['taxon'], animal['name'])
            print(nested_lookup.nested_lookup('name', tree))

            print(nested_lookup.nested_update(document, key='name', value='test'))
            exit(0)

            tree_entry = {}
            tree_entry['name'] = animal['name']
            tree_entry['taxon'] = animal['taxon']
            tree_entry['_id'] =  animal['_id']
            tree_entry['children'] = animal['children']

    return tree_entry

def build_tree(taxon, given_tree):

    tree = []
    my_tree = {}

    for animal_class in database:
        if animal_class['taxon'] == taxon:

            # now we have every genus, so we need to put the genus in the corresponding family
            parent = animal_class['parents'][-1]
            parent['children'] = []

            print(parent)

            # print(parent, animal['name'])
            dict_to_elevate = {}
            # now retrieve the subclass and all its children from our given_tree
            res = next((dict for dict in given_tree if dict['name'] == animal_class['name']), None)
            if res:
                dict_to_elevate = res
            else:
                print('panic')

            # for dict in given_tree:
            #     if dict['name'] == animal_class['name']:
            #         dict_to_elevate = dict

            # move the genus inside the parent in the tree

            # check if the parent already exists in the tree
            if not any(dict['name'] == parent['name'] for dict in tree):
                # if not, append it to the tree, including the child we are looking at
                parent['children'].append(dict_to_elevate)
                tree.append(parent)
            # if it does exist, we need to append the current animal to the children
            else:
                for dict in tree:
                    if dict['name'] == parent['name']:
                        dict['children'].append(dict_to_elevate)

    return tree

tree = { 'tree':[] }

# f = open('tree.json')
# tree = json.load(f)

# tree['tree'] = create_tree_from_animals()

f = open('myfile6.json')
database = json.load(f)
database = database['1']['animals']

taxa_list = [
    'genus',
    'family',
    'order',
    'superorder',
    'infraclass',
    'subclass',
    'class',
    'subphylum',
    'phylum',
    ]

# print(nested_lookup.nested_lookup('children', tree))

# exit(0)

tree = []

counter = 0

# first, we loop through all species and place them with their parents in a genus_tree
for animal in database:
    if animal['taxon'] == 'species':
        tree_entry = {}
        tree_entry['name'] = animal['name']
        tree_entry['taxon'] = animal['taxon']
        tree_entry['_id'] =  animal['_id']
        # record the parent
        parent = animal['parents'][-1]
        # check if the parent already exists in the tree
        if not any(dict['name'] == parent['name'] for dict in tree):
            # if not, append it to the tree, including the child we are looking at
            parent['children'] = [tree_entry]
            tree.append(parent)
        else:
            # find it in the list and append the child
            for dict in tree:
                if dict['name'] == parent['name']:
                    dict['children'].append(tree_entry)

# now we have a genus tree with species. we need to now build the rest of the tree from the ground up
genus_tree = copy.deepcopy(tree)

taxa_list = [
    'genus',
    'family',
    'order',
    'superorder',
    'infraclass',
    'subclass',
    'class',
    'subphylum',
    'phylum',
    ]

for taxon in taxa_list:
    tree = build_tree(taxon, tree)
    
    # print(tree)
    # exit(0)

out_file = open("tree2.json", "w")
json.dump(tree, out_file, indent = 2)
out_file.close()
