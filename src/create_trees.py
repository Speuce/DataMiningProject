import csv
from typing import List, Tuple

import numpy as np
from numpy import ndarray

from data_structs import Tree, create_basic_tree


def create_trees() -> Tuple[List[Tree], ndarray]:
    """
    Parses the bitmap_column_details for all data entries, and creates
    BASIC hierarchies by default. (one "ALL" parent, n children nodes)
    For advanced hierarchies, add the respective branches below
    """
    trees = []
    binary_index_table = np.empty(256, dtype=object)
    with open('bitmap_column_details.csv', newline='') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        curr: str = ""
        curr_tuples = []
        for i, row in enumerate(reader):
            # print(f"{i} : {row[1]}")
            # TODO create special trees for number/time of day
            if curr != row[1]:  # if we're already looking at that data type
                # finish old tree
                if curr_tuples:
                    trees.append(create_basic_tree(curr_tuples, curr, binary_index_table))

                # create new tree
                curr = row[1]
                curr_tuples = []
            # add to tree
            curr_tuples.append((i, row[2]))
    return trees, binary_index_table


trees, index = create_trees()
