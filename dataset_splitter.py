from recsys.datamodel.data import Data
from recsys.algorithm.factorize import SVD

filename = './data/movielens/ratings.dat'
data = Data()
format = {'col':0, 'row':1, 'value':2, 'ids': int}
data.load(filename, sep='::', format=format)
train, test = data.split_train_test(percent=80) # 80% train, 20% test

svd = SVD()
svd.set_data(train)
