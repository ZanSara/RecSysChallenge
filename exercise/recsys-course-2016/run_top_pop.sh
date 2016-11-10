#!/bin/bash

python3 converter.py --in
python3 main.py data/ml100k/ratings.csv --header 0 --recommender top_pop
python3 converter.py --out
