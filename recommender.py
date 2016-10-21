# -*- coding: utf-8 -*-

# Fundamental imports
import numpy as np
import scipy as sp

# Utility imports
from optparse import OptionParser
import csv

# Constants
TRAINING_SET = "full_datasets/"
TESTING_LOCAL_SET = "full_datasets/"
TESTING_FULL_SET = "full_datasets/"
SUBMISSION = "submission.csv"




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
    
    
    

###### LOADING DATASETS #####

# Interactions' structure
# user_id	item_id		interaction_type	created_at
print("\t# Loading interactions dataset...")
interactions_map = sp.genfromtxt("{}interactions.csv".format(test_set), dtype='int64', delimiter="\t")
print("\t  -> got {} rows".format(interactions_map.shape[0]))

# Item Profiles' structure
# id	title	career_level	discipline_id	industry_id	country	region	latitude	longitude	employment	tags	created_at	active_during_test
print("\t# Loading item profiles' dataset...")
with open("{}item_profile.csv".format(test_set), newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    item_profiles = np.array(list(csvreader))
print("\t  -> got {} rows".format(item_profiles.shape[0]))

# User Profiles' structure
# user_id	jobroles	career_level	discipline_id	industry_id	country	region	experience_n_entries_class	experience_years_experience	experience_years_in_current	edu_degree	edu_fieldofstudies
print("\t# Loading user profiles' dataset...")
user_profiles = sp.genfromtxt("{}user_profile.csv".format(test_set), dtype='int64', delimiter="\t")
print("\t  -> got {} rows".format(user_profiles.shape[0]))

# Target users' structure
# user_id
print("\t# Loading target users' dataset...")
target_users = sp.genfromtxt("{}target_users.csv".format(test_set), dtype='int64', delimiter="\t")
print("\t  -> got {} rows".format(target_users.shape[0]))
print("\t# Datasets loaded.")



#########  ALGORITHM - TopPop Refined  #########

item_codes_statuses = np.column_stack( (item_profiles[1:, 0], item_profiles[1:, -1]) )
# Keep only active items
item_codes_statuses = item_codes_statuses[item_codes_statuses[:, 1] == '1']

# Selects the row of interacting items and the row of ratings
interacting_items = interactions_map[1:,1:3]

# Sort interactions table to generate "clusters"
interacting_items = np.sort(interacting_items, axis=0)

# Count each block and store the top five frequencies
top_five = [[0, 0], [0,0], [0,0], [0,0], [0,0]]
buffer_item = [0, 0]
for i in range(interacting_items.shape[0]):
	if interacting_items[i][0] == buffer_item[0]:
		buffer_item[1] = buffer_item[1] + interacting_items[i][1]
	else:
		for index in range(0, 5):
			if top_five[index][1] < buffer_item[1]:
				top_five.insert(index, [buffer_item[0], buffer_item[1]])
				top_five.pop()
				break
		buffer_item[1] = 1
	buffer_item[0] = interacting_items[i][0]

recommendations = np.array(top_five)
print(top_five)




###### WRITE SUBMISSION FILE ###################

recommendations = ""
for rec in top_five:
	recommendations += "{} ".format(rec[0])	
	
with open(SUBMISSION, 'wb') as csvfile:
	csvfile.write(bytes("user_id,recommended_items\n", 'UTF-8'))	
	row = []
	for i in range(1, target_users.shape[0]):
		csvfile.write(bytes("{},{}\n".format(target_users[i], recommendations), 'UTF-8'))

print("{} wrote successfully. Bye!".format(SUBMISSION))

