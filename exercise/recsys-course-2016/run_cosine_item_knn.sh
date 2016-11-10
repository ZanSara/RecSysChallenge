#!/bin/bash

python3 converter.py --in
python3 main.py data/ml100k/ratings.csv --header 0 --recommender item_knn --params similarity=cosine,k=50,shrinkage=100
python3 converter.py --out
