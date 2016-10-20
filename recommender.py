# -*- coding: utf-8 -*-

# Fundamental imports
import numpy as np
import scipy as sp

from scipy.stats import itemfreq

# Utility imports
from optparse import OptionParser

# Constants
TRAINING_SET = "full_datasets/"
TESTING_LOCAL_SET = "full_datasets/"
TESTING_FULL_SET = "full_datasets/"
RESULT = "result.csv"




# Command-line parsing
parser = OptionParser()
parser.add_option("-f", "--test_full",
                  action="store_true", dest="full_test_set",
                  help="test the recommender on the full testing dataset.")
parser.add_option("-l", "--test_local",
                  action="store_false", dest="full_test_set", default=False,
                  help="test the recommender on the local testing dataset (default behavior).")

(options, args) = parser.parse_args()
if options.full_test_set:
    test_set = TESTING_FULL_SET
    print(" Full dataset chosen for testing")
else:
    test_set = TESTING_LOCAL_SET
    print(" Local dataset chosen for testing")
    
    
# Loading data
print("\t# Loading interactions dataset...")
interactions_map = sp.genfromtxt("{}interactions.csv".format(test_set), delimiter="\t")
print("\t  -> got {} rows".format(interactions_map.shape[0]))
print("\t# Loading item profiles' dataset...")
item_profiles = sp.genfromtxt("{}item_profile.csv".format(test_set), delimiter="\t")
print("\t  -> got {} rows".format(item_profiles.shape[0]))
#print("\t# Loading user profiles' dataset...")
#user_profiles = sp.genfromtxt("{}user_profile.csv".format(test_set), delimiter="\t")
#print("\t  -> got {} rows".format(user_profiles.shape[0]))
#print("\t# Loading target users' dataset...")
#target_users = sp.genfromtxt("{}target_users.csv".format(test_set), delimiter="\t")
#print("\t  -> got {} rows".format(target_users.shape[0]))
print("\t# Datasets loaded.")



##### First try with a TopPop Algorithm ######

item_codes = item_profiles[:, 0]
item_codes = item_codes[~sp.isnan(item_codes)]

# Selects the row of interacting items: each interactions put an entry here.
interacting_items = interactions_map[:,1]
interacting_items = interacting_items[~sp.isnan(interacting_items)]

# Sort table!
print(" # Sorting results...")
interacting_items = interacting_items[interacting_items[:].argsort()]
print(" # Sort completed!")

# Count each block and store the top five frequencies
top_five = [[0, 0], [0,0], [0,0], [0,0], [0,0]]
buffer_item = [0, 0]
count = 0

for item in interacting_items:
	if item == buffer_item[0]:
		buffer_item[1] = buffer_item[1] + 1
	else:
		for index in range(0, 5):
			if top_five[index][1] < buffer_item[1]:
				top_five.insert(index, [buffer_item[0], buffer_item[1]])
				top_five.pop()
				break
		buffer_item[1] = 1
	buffer_item[0] = item

print(top_five)



# Create the submission file
print("\t# Loading submissions' file template...")
submission = sp.genfromtxt("sample_submission.csv", delimiter=",")
print("\t  -> got it!".format(item_profiles.shape[0]))

recommendations = ""
for rec in top_five:
	recommendations += "{} ".format(rec[0])
	
#for row in submission:
#	row[1] = recommendations

print(recommendations)
#np.savetxt("submission.csv", submission, delimiter=",")






##### Try with the Global Effects Algorithm ######

# Extract useful data
#interacting_users = interactions_map[:,0]
#interacting_users = interacting_users[~sp.isnan(interacting_users)]
#interacting_items = interactions_map[:,1]
#interacting_items = interacting_items[~sp.isnan(interacting_items)]
#interactions_values = interactions_map[:,2]
#interactions_values = interactions_values[~sp.isnan(interactions_values)]

# Average Rating (Mu)
#sum_of_interactions = sp.sum(interactions_values)
#num_of_valid_interactions = interactions_values.shape[0] - sp.sum(sp.isnan(interactions_values))
#mu = np.divide(sum_of_interactions, num_of_valid_interactions)
#print(" # Computing MU: Sum is {}, num is {} -----> mu seems to be {}".format(sum_of_interactions, num_of_valid_interactions, mu))

# Item Biases (Bi)

#item_ratings_matrix = np.matrix() # gonna have this structure: item - sum_ratings - n_ratings

#item_rating_matrix[:,0] = interacting_items
#item_rating_matrix[:,1] = 

