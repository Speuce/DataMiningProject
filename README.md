# DataMiningProject

Multidimensional Multilevel Quantitative Association Rule Mining with UK Traffic Accident data.

## About

The purpose of this project is to mine frequent itemsets and association rules with the UK government's traffic accident database. The data is updated annually at [this](https://data.gov.uk/dataset/cb7ae6f0-4be6-4935-9277-47e5ce24a11f/road-safety-data) page. A subset of the data is also available through [Kaggle](https://www.kaggle.com/silicon99/dft-accident-data).

The algorithm applied to this dataset is based off the paper _[Mining Multi-Dimensional and Multi-Level Sequential
Patterns](https://hal-lirmm.ccsd.cnrs.fr/lirmm-00617320/file/jal_m2sp-2.pdf)_. There are a few key differences between our implementation and the algorithm as described in the paper:

1. Our implemenation ignores the temporal dimension as described in the paper and does not mine sequences.
2. Our algorithm does not support more than one reference dimension, nor more than one entry per block.
3. Our implementation mines all frequent itemsets, rather than maximal atomic frequent sequences, as described in the paper.

## Tools Used

Our implementation is written in Python, and uses Numpy to manipulate and mine the data. 


The data was cleaned/mapped to individual columns using SQL queries. These queries are available in the SQL.txt file.

## Cleaning and Formatting Data

'Casualty' was used as our reference dimension, and as such we essentially used `casualty natural join vehicle natural join accident` as our dataset.

Next, the data was limited to those that occured between 2005-2017 so that our data would be comparable to [this paper](). Then the data was mapped to individual boolean columns according to their value. For example, if the accident occured at a speed limit of 30, the corresponding entry would have `speed_limit_30` set to True`. This way, each entry can be formatted as a list of true/false values -- binary!

Next, the data was converted to a compressed numpy array using `python create_data.py` with `bitmap_sample.csv` as the default input. The input is hardcoded in and can be changed as you need it. By default, the data is saved into `/src/bitmap_sample_result.npy`.

At this point, the data is ready for use.

## How to Use

Aside from the cleaned and formatted data in a numpy array file, a csv was also created to map binary indicies to corresponding column names from the original table. This is file is `bitmap_column_details.csv`.

The data can be mined by running `python mine_data.py` which by default takes in the `bitmap_column_details.csv` and `bitmap_sample_result.npy` files as mentioned earlier. The minimum support threshold can be set at the top of `mine_data.py` by changing the MINSUP variable to the desired value.

  **Caution:** setting a low minsup value can lead to _very_ long runtimes.

Running `mine_data` creates two log files. The first (`log_all_accidents.log`) tracks ALL frequent itemsets, the second (`log_all_accidents_reduced.log`) tracks only the frequent itemsets that have no frequent subsets. (in other words, itemsets that are supersets of other itemsets are ignored).

Finally, the resultant log file should by run through `python clean_sort_fisets.py` in order to remove duplicate entries and sort the frequent itemsets lexicographically. By default `clean_sort_fisets.py` runs on `src/log_all_accidents.log` and outputs the result in `result/all_accidents_sorted.txt`.

Once the data has been obtained from the previous algorithms using the `rule_analyze.py` file the individual rules can be obtained.  At the moment this requires manual editing of the file input.  This can be set to the data output files such as `all_accidents.txt` which will then output a text file consisting of the rules generated plus their associated confidence values to `result\all_accident_rules.txt`.

## Approximate Runtimes

On a modern-day 2.6Ghz 6 core intel i7 processor:
- With the full dataset containing 2,755,286 entries, and using a minsup of 30%, the algorithm finished in approximately 4 hours.
- Using a subset of the data (filtered to only include fatal accidents) with 49,191 entries, using a minsup of 15%, the algorithm finished in approximately 45 minutes.
