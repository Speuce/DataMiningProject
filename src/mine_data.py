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
                    #print(f'{node.verbose_name}, sup: {node.count}')
                    itemset = np.copy(all_alls)
                    itemset[i] = node
                    L1.append(itemset)
    # TODO run algo2

def get_rec_maf_seq(set_a, minsup, block_set, MAFS):
    cand = generated_set(a) #we've already pruned infrequent nodes from the tree, so we don't have to check if the dimensions are individually frequent
    freq = []#TODO remove all elements of cand that aren't frequent (how to check the frequencies?)
    if len(freq) == 0:
        #if for every set a' in MAFS a is not more specific than a' (double check)
            #then, add a to MAFS
    else:
        for alpha in freq:
            #get the set of all tuples c in the block_set where c.DA is more specific than alpha
            sigma_blockset = [] #??? TODO
            get_rec_maf_seq(alpha,minsup,sigma_blockset, MAFS)




def generated_set(input_set):
    # first we get p(a)  , which is the last dimension that isn't an ALL.
    #The lowest p(a) can be is -1, but this gives the same behaviour as p(a) = 0, so we set p(a) = 0 as the minimum
    p = input_set.size-1
    while(input_set[p].index == 0 and p > 0): #the node at p is an all category if its index (on the tree) is 0
        p -= 1

    #now we actually create gen(a)

    gen = []
    for i in range(p,input_set.size):
	    gen = gen + down_set(input_set,i)
    return gen

def down_set(in_array, index):
    #NOTE input is an array of tree nodes
    old_node = in_array[index]
    down_nodes = old_node.tree.get_children(old_node)
    print(len(down_nodes))
    if len(down_nodes) == 0:
	    return []
    else:
        down_set = []
	    #create a set for every value in down(delta(i)), where delta(i) in a is replaced
	    #with that value from down(delta(i))
        for down_node in down_nodes:
            down_set.append([down_node if i==index else in_array[i] for i in range(len(in_array))])
        return down_set

a = np.load("src/data_uint.npy")
trees, bit_index_table = create_trees()
algorithm_one(a, trees, bit_index_table)
