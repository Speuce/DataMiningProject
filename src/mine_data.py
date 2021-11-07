from typing import List

import numpy as np
from numpy import ndarray

from src.create_trees import create_trees
from src.data_structs import Tree, TreeNode


def algorithm_one(blocks: ndarray, trees: List[Tree], bit_index_table: ndarray):
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
        print(sup)


a = np.load("./test.npy")
trees, bit_index_table = create_trees()
print(a)
algorithm_one(a, trees, bit_index_table)
