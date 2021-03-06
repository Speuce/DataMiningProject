import csv
from typing import List, Tuple, Set

import numpy as np
from numpy import ndarray

from data_structs import Tree, create_basic_tree, TreeNode


def create_trees(filepath: str, ignore_casualty_severity: bool=False) -> Tuple[List[Tree], ndarray]:
    """
    Parses the bitmap_column_details for all data entries, and creates
    BASIC hierarchies by default. (one "ALL" parent, n children nodes)
    For advanced hierarchies, add the respective branches below
    """
    trees = []
    ignored_values = ['None within 50 metres',
                      'No physical crossing facilities within 50 metres',
                      'Not at junction or within 20 metres',
                      'Fine no high winds',
                      'Dry']
    ignored_dimensions = ['accident_severity',
                          'vehicle_type',
                          'casualty_class'
                          ]
    if ignore_casualty_severity:
        ignored_dimensions.append('casualty_severity')
    binary_index_table = np.empty(256, dtype=object)
    with open(filepath, newline='') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        curr: str = ""
        curr_tuples = []
        for i, row in enumerate(reader):
            # print(f"{i} : {row[1]}")
            if row[1] not in ignored_dimensions:
                if curr != row[1]:  # if we're already looking at that data type
                    # finish old tree
                    if curr_tuples:
                        if curr == 'vehicle_type' or curr == 'casualty_type':
                            trees.append(create_vehicle_type_tree(curr_tuples, curr, binary_index_table))
                        elif curr == 'age_band_of_casualty' or curr == 'age_band_of_driver':
                            trees.append(create_age_band_tree(curr_tuples, curr, binary_index_table))
                        elif curr == 'age_of_vehicle':
                            trees.append(create_age_of_vehicle_tree(curr_tuples, curr, binary_index_table))
                        else:
                            trees.append(create_basic_tree(curr_tuples, curr, binary_index_table))

                    # create new tree
                    curr = row[1]
                    curr_tuples = []
                # add to tree
                if row[2] not in ignored_values:
                    curr_tuples.append((i, row[2]))
    return trees, binary_index_table


def create_vehicle_type_tree(tuples, name: str, binary_index_table) -> Tree:
    ret = Tree(branch_factor=6, verbose_name=name, levels=3)
    keywords_dict = {
        'Motorcycle Occupant': ['otorcycle'],
        'Car/Taxi Occupant': ['Car', 'Taxi'],
        'Van/Truck Occupant': ['Van', 'Goods'],
        'Public Transport': ['Bus', 'Minibus', 'Tram'],
        'Sidewalk User': ['Cyclist', 'Pedal', 'Pedestrian', 'Mobility'],
        'Other': ['Agri', 'orse', 'Other', ],
    }
    treenode_dict = {ret.add_node(set(), name + ":" + keyword): values for (keyword, values) in keywords_dict.items()}
    for (bin_index, verbose_name) in tuples:
        found = False
        for (key, values) in treenode_dict.items():
            for keyword in values:
                if keyword in verbose_name:  # MATCH Found!
                    binary_index_table[bin_index] = ret.add_child_node({bin_index}, name + ":" + verbose_name, key)
                    found = True
                    break
            if found:
                break
        else:
            print(f'Could not match with item {verbose_name}!')
            raise Exception
    return ret


def create_age_band_tree(tuples, name: str, binary_index_table) -> Tree:
    ret = Tree(branch_factor=4, verbose_name=name, levels=3)
    # ASSUMING TUPLES ARE ORDERED BY AGE BAND
    treenodes = [ret.add_node(set(), name + ":" + keyword) for keyword in ['Child', 'Youth', 'Adult', 'Senior']]
    for i, (bin_index, verbose_name) in enumerate(tuples):
        parent = None
        if i <= 2:
            parent = treenodes[0]
        elif i <= 4:
            parent = treenodes[1]
        elif i <= 7:
            parent = treenodes[2]
        else:
            parent = treenodes[3]

        binary_index_table[bin_index] = ret.add_child_node({bin_index}, name + ":" + verbose_name, parent)
    return ret


def add_to_tree(tree: Tree, item: Tuple[int, str], name: str, binary_index_table, parent: TreeNode):
    index, node_name = item
    node = tree.add_child_node({index}, name + ":" + node_name, parent)
    binary_index_table[index] = node
    return node


def create_age_of_vehicle_tree(tuples, name: str, binary_index_table) -> Tree:
    ret = Tree(branch_factor=3, verbose_name=name, levels=6)

    parent = ret.get_root_node()
    parent_1 = ret.add_child_node(set(), name + ":???9", parent)
    parent_2 = ret.add_child_node(set(), name + ":10-19", parent)
    parent_3 = ret.add_child_node(set(), name + ":20+", parent)

    add_to_tree(ret, tuples[-5], name, binary_index_table, parent_2)
    add_to_tree(ret, tuples[-4], name, binary_index_table, parent_2)

    add_to_tree(ret, tuples[-3], name, binary_index_table, parent_3)
    add_to_tree(ret, tuples[-2], name, binary_index_table, parent_3)
    add_to_tree(ret, tuples[-1], name, binary_index_table, parent_3)

    parent = parent_1

    add_to_tree(ret, tuples[-6], name, binary_index_table, parent)
    parent = ret.add_child_node(set(), name + ":???7", parent)
    add_to_tree(ret, tuples[-7], name, binary_index_table, parent)
    parent = ret.add_child_node(set(), name + ":???5", parent)
    add_to_tree(ret, tuples[-8], name, binary_index_table, parent)
    parent = ret.add_child_node(set(), name + ":<3", parent)
    add_to_tree(ret, tuples[-9], name, binary_index_table, parent)
    add_to_tree(ret, tuples[-10], name, binary_index_table, parent)

    return ret

