import json
import copy

def build_tree(taxon, given_tree):

    tree = []

    for animal_class in database:
        if animal_class['taxon'] == taxon:

            # now we have every genus, so we need to put the genus in the corresponding family
            try:
                parent = animal_class['parents'][-1]
            except:
                print('no parents available, break and use tree')
                return given_tree
            
            parent['children'] = []
            # print(parent, animal['name'])
            dict_to_elevate = {}
            # now retrieve the subclass and all its children from our given_tree
            res = next((dict for dict in given_tree if dict['name'] == animal_class['name']), None)
            if res:
                dict_to_elevate = res
            else:
                print('no parents available, break and use tree')
                return given_tree
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
database = database['2']['animals']

taxa_list = [
    'genus',
    'tribe',
    'subfamily',
    'family',
    'order',
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

# print(tree)
# exit(0)

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

out_file = open("tree3.json", "w")
json.dump(tree, out_file, indent = 2)
out_file.close()
