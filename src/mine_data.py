from typing import List

import numpy as np
from numpy import ndarray

from create_trees import create_trees
from data_structs import TreeNode, Tree

MINSUP = 1


def algorithm_one(blocks: ndarray, trees: List[Tree], bit_index_table: ndarray):
    ### PART ONE -- Compute individual item counts
    curr_slice_num = -1
    curr_slice = None
    i: int
    node: TreeNode
    for (i, node) in enumerate(bit_index_table):
        if not node:
            continue
        # since we are iterating inidividual bit values, we don't need all 32-bit sections,
        # this if statement is just to grab the individual 32-bit section instead of the whole thing.
        if i // 32 > curr_slice_num:
            curr_slice_num = i // 32
            curr_slice = blocks[:, curr_slice_num]
        # get the bit string to AND each value with from the node
        and_with = node.select_array[curr_slice_num]

        # numpy handles operations wonderfully
        # this gets the support for each individual item
        sup = np.count_nonzero(curr_slice & and_with)

        # iterate through parents and update count as well
        curr = node
        while curr:
            curr.add_count(sup)
            curr = curr.tree.get_parent_node(curr)

    ### Pre-part two -- create a list containing every ALL_x item
    all_alls = np.empty(len(trees), dtype=object)
    tree: Tree
    for i, tree in enumerate(trees):
        all_alls[i] = tree.get_root_node()

    ### PART TWO -- COMPUTE L1/PRUNE INFREQUENT NODES
    L1 = []
    tree: Tree
    for i, tree in enumerate(trees):
        for node in tree.all_nodes():
            if node.index != 0:  # don't know if we should be pruning root nodes (ALL_x)
                if node.count < MINSUP:
                    # TODO prune node
                    pass
                else:
                    print(f'{node.verbose_name}, sup: {node.count}')
                    itemset = np.copy(all_alls)
                    itemset[i] = node
                    L1.append(itemset)
    # TODO run algo2



a = np.load("src/data_uint.npy")
trees, bit_index_table = create_trees()
algorithm_one(a, trees, bit_index_table)
