import logging
import threading
from typing import List

import numpy as np
from numpy import ndarray

from create_trees import create_trees
from data_structs import TreeNode, Tree

# MINSUP = 7370
# MINSUP = 61878
MINSUP = 413293
output_path = './log_all_accidents'
input_path = '../data/data_uint32.npy'
column_detail_path = '../data/bitmap_column_details.csv'
casualty_severity = True

THREAD = 0


def algorithm_one(blocks: ndarray, trees: List[Tree], bit_index_table: ndarray):
    global THREAD
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
            if node.index > 0:  # don't know if we should be pruning root nodes (ALL_x)
                if node.count < MINSUP:
                    node.tree.remove_node(node)
                else:
                    # print(f'{node.verbose_name}, sup: {node.count}')
                    itemset = np.copy(all_alls)
                    itemset[i] = node
                    L1.append((itemset, node.count))
                    # print(f'{node.verbose_name}||{node.count}')
    sum = 0
    for tree in trees:
        sum += len(tree.all_nodes())

    print(f'Running algo on: {sum} nodes.')

    MAFS = []
    threads = []

    for i, a in enumerate(L1):
        THREAD += 1
        # get_rec_maf_seq(a, MINSUP, blocks, MAFS, False, None, THREAD)
        if i > 7:
            THREAD += 1
            x = threading.Thread(target=get_rec_maf_seq, args=(a, MINSUP, blocks, MAFS, False, None, THREAD))
            threads.append(x)
        else:
            get_rec_maf_seq(a, MINSUP, blocks, MAFS, True, threads)

    print(f'starting {THREAD} threads...')
    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()
    print('done.')


def get_rec_maf_seq(a, minsup, block_set, MAFS, stuff=False, threads=None, thread_num=-1):
    global THREAD
    set_a, sup_a = a
    cand = generated_set(set_a)
    # we've already pruned infrequent nodes from the tree, so we don't have to check if the dimensions are individually frequent
    freq = []
    for ax in cand:
        sup = compute_support(block_set, ax)
        if sup >= minsup:
            freq.append((ax, sup))

    print_tree_list(set_a, sup_a)
    if len(freq) == 0:
        print_tree_list_2(set_a, sup_a)
    else:
        for i, alpha in enumerate(freq):
            # #get the set of all tuples c in the block_set where c.DA is more specific than alpha
            # sigma_blockset = [] #??? TODO
            if stuff:
                THREAD += 1
                threads.append(
                    threading.Thread(target=get_rec_maf_seq, args=(alpha, MINSUP, block_set, MAFS, False, THREAD))
                )
            else:
                get_rec_maf_seq(alpha, minsup, block_set, MAFS)
    if thread_num != -1:
        print(f'thread finished: {thread_num}')


def compute_support(block_set: ndarray, search_tuple: List[TreeNode]) -> int:
    query = compute_query_param(search_tuple)
    res = np.bitwise_and(block_set, query[:, None])
    sup = np.sum(np.transpose(res.any(axis=2)).all(axis=1))
    return int(sup)


def compute_query_param(tupl: List[TreeNode]) -> ndarray:
    return np.array([item.select_array for item in tupl if item.index > 0])


def generated_set(input_set: List[TreeNode]):
    # first we get p(a)  , which is the last dimension that isn't an ALL.
    # The lowest p(a) can be is -1, but this gives the same behaviour as p(a) = 0, so we set p(a) = 0 as the minimum
    p = len(input_set) - 1
    try:
        while (input_set[p].index == 0 and p > 0):  # the node at p is an all category if its index (on the tree) is 0
            p -= 1
    except:
        print("error :(")

    # now we actually create gen(a)

    gen = []
    for i in range(p, len(input_set)):
        next = down_set(input_set, i)
        # for n in next:
        #     print_tree_list(n)
        gen += next
    return gen


def down_set(in_array: List[TreeNode], index):
    # NOTE input is an array of tree nodes
    old_node = in_array[index]
    down_nodes = old_node.tree.get_children(old_node)
    # print(len(down_nodes))
    if len(down_nodes) == 0:
        return []
    else:
        down_set = []
        # create a set for every value in down(delta(i)), where delta(i) in a is replaced
        # with that value from down(delta(i))
        for down_node in down_nodes:
            down_set.append([down_node if i == index else in_array[i] for i in range(len(in_array))])
        return down_set


def print_tree_list(lis: List[TreeNode], sup: int = -1):
    str_1 = ''
    for node in lis:
        if node.index != 0:
            str_1 += node.verbose_name + ","
    logger.info(f'{str_1}|{sup}')


def print_tree_list_2(lis: List[TreeNode], sup: int = -1):
    str_1 = ''
    for node in lis:
        if node.index != 0:
            str_1 += node.verbose_name + ","
    logger2.info(f'{str_1}|{sup}')


def setup_logger(name, log_file, level=logging.INFO):
    """To setup as many loggers as you want"""

    handler = logging.FileHandler(log_file, mode='w')
    handler.setFormatter(logging.Formatter('%(message)s'))

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger


logger = setup_logger('logger1', f'{output_path}.log')
logger2 = setup_logger('logger2', f'{output_path}_reduced.log')

a = np.load(input_path)
trees, bit_index_table = create_trees(column_detail_path, not casualty_severity)
algorithm_one(a, trees, bit_index_table)
