# -*- coding: utf-8 -*-

# Fundamental imports
import numpy as np
import scipy as sp

# Utility imports
from optparse import OptionParser
import csv

# Constants
SUBMISSION = "submission.csv"



def recommend(interactions_map, item_profiles, user_profiles, target_users):

	#########  ALGORITHM - TopPop Refined  #########
	
	item_codes_statuses = np.column_stack( (item_profiles[:, 0], item_profiles[:, -1]) )
	# Keep only active items
	item_codes_statuses = item_codes_statuses[item_codes_statuses[:, 1] == '1']

	# Selects the row of interacting items and the row of ratings
	interacting_items = interactions_map[:,1:3]

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

	recommendations = ""
	for rec in top_five:
		recommendations += "{} ".format(rec[0])	
	
	rec_matrix = []
	for i in range(target_users.shape[0]):
		rec_matrix.append(recommendations)
	
	return zip(target_users, rec_matrix)
	
	
	
def writecsv(user_rec, target_users):
	
	###### WRITE SUBMISSION FILE ###################
	
	with open(SUBMISSION, 'wb') as csvfile:
		csvfile.write(bytes("user_id,recommended_items\n", 'UTF-8'))	
		row = []
		for item in user_rec:
			csvfile.write(bytes("{},{}\n".format(item[0], item[1]), 'UTF-8'))

	print(" # {} wrote successfully. Bye!".format(SUBMISSION))

