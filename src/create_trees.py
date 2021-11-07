import csv
from typing import List, Optional

from src.data_structs import Tree, create_basic_tree


def create_trees() -> List[Tree]:
    trees = []
    with open('../bitmap_column_details.csv', newline='') as csvfile:
        next(csvfile)
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        curr: str = ""
        curr_tuples = []
        for i, row in enumerate(reader):
            print(f"{i} : {row[1]}")
            # TODO create special trees for number/time of day
            if curr == row[1]:  # if we're already looking at that data type
                # add to tree
                curr_tuples.append((i, row[2]))
            else:
                # finish old tree
                if curr_tuples:
                    trees.append(create_basic_tree(curr_tuples, curr))

                # create new tree
                curr = row[1]
                curr_tuples = []
    return trees


trees = create_trees()
print(trees)
