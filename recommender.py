# -*- coding: utf-8 -*-

# Fundamental imports
import numpy as np
import scipy as sp
import pandas as pd

# Utility imports
from optparse import OptionParser
import csv
import time

# Constants
SUBMISSION = "submission.csv"




def recommend(interactions_map, item_profiles, user_profiles, target_users):
	
	return recommendTopPop(interactions_map, item_profiles, user_profiles, target_users)

	
	#print(interactions_map.groupby('item_id').size()[:10])
	#print(interactions_map.item_id.value_counts()[:5])
	top_rated = interactions_map.item_id.value_counts()[:5].index
	print("Top Rated: {}".format(top_rated))
	
	print("Creating recommendations table...")
	rec_matrix = pd.DataFrame(columns=['recs'], index = target_users.user_id )
	for i in range(rec_matrix.shape[0]):
		rec_matrix.iloc[i].recs = list(top_rated)
	print("Recommendations created!")
	#print(rec_matrix[:10])
	return rec_matrix
	
	
	
	
	
	return recommendTopPop(interactions_map, item_profiles, user_profiles, target_users)

	#########  ALGORITHM - Bare Contex-Based  #########
	##
	## 					Similarity:
	##         S_ij  =  v_i*v_j / (|v_i|*|v_j|+k)
	##
	## 				  Predicted rating:
	##      R_ui  =  ∑(j) (r_uj * S_ij) / ∑(j) S_ij
	##  
	####################################################
	
	rec_matrix = []
	for u in 5: #range(target_users.shape[0]):
		
		# Find items he interacted with
		# Remove all expired entries and interacted items from candidate list
		# Find the most 50 items most similar to the interacted ones and rank them
		# Take first 5 and recommend them
		
		
		# Find items the user interacted with - the j items
		interactions = interactions_map[:,0:1]
		interactions = np.sort(interactions, axis=0)
		
		j_items = []
		for i in range(interactions_map.shape[0]):
			if interactions_map[i][1] != j_items[len(j_items)-1]:
				j_items.append(interactions_map[i][1])
		
		print(j_items)
		
		
		predicted_ratings = [] # take the 50 most similar!
		#for item in item_profiles:
			
			#similarity
				
			
			#predicted_ratings.append([ item, prediction ])
			
		#rec_matrix = []
		#rec_matrix.append([user, recommendations])
	
	return np.array(rec_matrix)






def recommendTopPop(interactions_map, item_profiles, user_profiles, target_users):

	#########  ALGORITHM - TopPop Refined  #########
	
	item_codes_statuses = item_profiles[['id', 'active_during_test']]
	# Keep only active items
	item_codes_statuses = item_codes_statuses.loc[item_codes_statuses.active_during_test == 1]
	
	# Selects the row of interacting items and the row of ratings
	interacting_items = interactions_map.drop('created_at', 1)

	# Sort interactions table to generate "clusters"
	#interacting_items = np.sort(interacting_items, axis=0)

	# Count each block and store the top 20 frequencies
	top_popular = interacting_items.groupby('item_id').sum().sort(['interaction_type'], ascending=False)
	top_popular = top_popular.index
	print(top_popular)
	
	#top_twenty = [[0, 0] for x in range(50)]
	#buffer_item = [0, 0]
	
	#for i in range(interacting_items.shape[0]):
		#if interacting_items[i][1] == buffer_item[0]:
			#buffer_item[1] = buffer_item[1] + interacting_items[i][2]
			#if interacting_items[i][2] == 3 and interacting_items[i][0] not in top_twenty[buffer_item[2]][2]:
				#try:
					#top_twenty[buffer_item[2]][2].append([interacting_items[i][0]])
				#except:
					#print("Eccezione! {}: {} - {}".format(buffer_item[2], len(top_twenty), top_twenty[1]))
					#return 0
		#else:
			#for index in range(0, 50):
				#if top_twenty[index][1] < buffer_item[1]:
					#top_twenty.insert(index, [buffer_item[0], buffer_item[1], []])
					#top_twenty.pop()
					#buffer_item[2] = index
					#break
			#buffer_item[1] = 1
		#buffer_item[0] = interacting_items[i][1]

	#r = [ [item[0], item[1]] for item in top_twenty ]
	#recommendations = np.array(r)
	#print("top_five: {} ".format(recommendations[:5]))
	
	print("Finding sent CVs...")
	cv_sent = interactions_map[['user_id', 'item_id', 'interaction_type']].loc[interactions_map.interaction_type == 3]
	cv_sent = cv_sent.set_index('item_id')
	cv_sent = cv_sent.groupby('user_id')
	print("Found!")
	
	print("Creating recommendations...")
	rec_matrix = pd.DataFrame(index=target_users.user_id, columns=['recs'])
	
	a = 0
	start = time.time()
	for user in target_users.user_id:
		a += 1
		try:
			recommendations = []
			counter = 0
			if user not in cv_sent.groups.keys():
				recommendations = [ rec for rec in top_popular[:5]]
			else:
				for rec in top_popular:
					if counter >= 5:
						break
					if rec not in cv_sent.groups[user]:
						recommendations.append(rec)
						counter +=1
				
			rec_matrix.loc[user, 'recs']= recommendations
		except KeyboardInterrupt:
			end = time.time()
			print("needed {:.2f}sec to reach {:.2f}% of calculations".format(end-start, a*100/target_users.shape[0]) )
			break
	print("Recommendations created!")
	print(rec_matrix[:20])
	
	return rec_matrix
	
	
	
	
def writecsv(user_rec, target_users):
	
	###### WRITE SUBMISSION FILE ###################
	
	with open(SUBMISSION, 'wb') as csvfile:
		csvfile.write(bytes("user_id,recommended_items\n", 'UTF-8'))	
		for item in user_rec.itertuples():
			csvfile.write(bytes("{},{}\n".format(item[0], " ".join( str(item[1])[1:-2].split(', ')) ), 'UTF-8'))

	print(" # {} wrote successfully. Bye!".format(SUBMISSION))

