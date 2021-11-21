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

Next, the data can be converted to a compressed numpy array using `python create_data.py` with `bitmap_sample.csv` as the default input. The input is hardcoded in and can be changed as you need it. By default, the data will be saved into `/src/bitmap_sample_result.npy`.

Now the data is ready for use!

## How to Use

## Approximate Runtimes
