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



def recommend(interactions_map, item_profiles, user_profiles, target_users):

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
	print("top_five: {} ".format(top_five))


	###### WRITE SUBMISSION FILE ###################

	recommendations = ""
	for rec in top_five:
		recommendations += "{} ".format(rec[0])	
		
	with open(SUBMISSION, 'wb') as csvfile:
		csvfile.write(bytes("user_id,recommended_items\n", 'UTF-8'))	
		row = []
		for i in range(1, target_users.shape[0]):
			csvfile.write(bytes("{},{}\n".format(target_users[i], recommendations), 'UTF-8'))

	print(" -> {} wrote successfully. Bye!".format(SUBMISSION))

