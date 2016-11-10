# -*- coding: utf-8 -*-

# Fundamental imports
import numpy as np
import scipy as sp
import pandas as pd

# Utility imports
from optparse import OptionParser
import csv
import time
from operator import itemgetter

# Constants
SUBMISSION = "submission.csv"




def recommend(interactions_map, item_profiles, user_profiles, target_users):
	
	############## OLDER ALGS TO RUN FOR COMPARISON ##################################
	
	#return recommendTopPop(interactions_map, item_profiles, user_profiles, target_users)
	#return recommendTopPopNP(interactions_map, item_profiles, user_profiles, target_users)


	#(n*m)(m*p) = (n*p)
	#(n*1)(1*p) = (n*p)
	#(1*m)(m*1) = (1*1)


	#########  ALGORITHM - Bare Contex-Based  ###########   
	##
	## 					Similarity:
	##         S_ij  =  v_i*v_j / (|v_i|*|v_j|+k)
	##
	## 				  Predicted rating:
	##      R_ui  =  ∑(j) (r_uj * S_ij) / ∑(j) S_ij
	##  
	######################################################
	
	
	# Find the 1000 top popular (temporary to make the alg running in a reasonable amout of time)
		
	# Selects the row of interacting items and the row of ratings
	interacting_items = interactions_map.drop('created_at', 1)
	interacting_items = interacting_items.drop('user_id', 1)
	# Keep only active items
	item_codes_statuses = item_profiles[['id', 'active_during_test']]
	item_codes_statuses = item_codes_statuses.loc[item_codes_statuses.active_during_test == 1]
	interacting_items = interacting_items[~interacting_items.item_id.isin(item_codes_statuses.id)]
	# Count each block and store the top frequencies
	top_pop = interacting_items.groupby('item_id').sum().sort(['interaction_type'], ascending=False)
	top_pop = top_pop.index[:10]
	print("1000 Top Pop: {}\n\n".format(top_pop))
	
	
	# Generate similiarity matrix S
	# Shape:
	#  	    i1   i2   i3
	#	i1  s11  s12  s13
	#	i2  s21  s22  s23
	#
	tpdf = pd.DataFrame(top_pop)
	sim = np.dot(tpdf, tpdf.T)
	S = pd.DataFrame(sim, index=top_pop, columns=top_pop)
	#print(S.head())
	
	# Generate sortable list of list
	# Shape:
	# 		similarities
	#   i1	[ (i1, s11), (i2, s12), (i3, s13), ... ]
	#   i2	[ (i1, s21), (i2, s22), (i3, s23), ... ]
	#   i3	[ (i1, s31), (i2, s32), (i3, s33), ... ]
	s_2_dict = S.to_dict()
	sortable_S = pd.Series(s_2_dict)
	sortable_S = sortable_S.apply(lambda x: x.items())
	sortable_S = sortable_S.apply(lambda x: sorted(x, key=itemgetter(0), reverse=True ))
	
	#for row in sortable_S:
	#	item = sorted([(k, v) for (k,v) in row.items()], reverse=True)
	
	print(sortable_S)
	print('-------------')
	
	
	# Remove interactions not related to the 1000 top pop
	print(interacting_items.info())
	interacting_items = interacting_items[~interacting_items.item_id.isin(top_pop)]
	print(interacting_items.info())
	
	# Group by user the interactions table
	interactions_grouped = interacting_items.groupby('user_id')
	
	
	# K of the KNN
	K = 5
	
	for k, user in enumerate(target_users.iterrows()):
		for item in top_pop:
			break
			# Sorto la riga delle somiglianze di i con tutti i j
			# trovo i top K j di cui l-utente ha dato un rating (ruj esiste)
			# applico la sommatoria e trovo Rui
			# salvo rui e passo all-elemento successivo
			
			#sorted_j = sim.loc()
	
	
	
	
	#rec_matrix = []
	#for i, user in enumerate(target_users):
		
		## Find items he interacted with
		## Remove all expired entries and interacted items from candidate list
		## Find the most 50 items most similar to the interacted ones and rank them
		## Take first 5 and recommend them
		
		
		## Find items the user interacted with - the j items
		##interactions = interactions_map[['user_id', 'item_id']]
		
		## Find active items
		#active_items = item_profiles.loc[item_profiles.active_during_test == 0]
		
		## Remove unactive items from interactions
		#ineractions_map = interactions_map.set_index('user_id')
		#active_items_interactions = interactions_map[~interactions_map['item_id'].isin(active_items['id'])]
		
		## Group
		#active_items_interactions = active_items_interactions.groupby(['user_id'])
		
		#for k, gp in enumerate(active_items_interactions):
			#if k>5: break
			#print('---------')
			#print(gp)
			
			
			
			
		## base similarity matrix (all dot products)
		## replace this with A.dot(A.T).toarray() for sparse representation
		#similarity = np.dot(A, A.T)

		## squared magnitude of preference vectors (number of occurrences)
		#square_mag = numpy.diag(similarity)

		## inverse squared magnitude
		#inv_square_mag = 1 / square_mag

		## if it doesn't occur, set it's inverse magnitude to zero (instead of inf)
		#inv_square_mag[numpy.isinf(inv_square_mag)] = 0

		## inverse of the magnitude
		#inv_mag = numpy.sqrt(inv_square_mag)

		## cosine similarity (elementwise multiply by inverse magnitudes)
		#cosine = similarity * inv_mag
		#cosine = cosine.T * inv_mag
			
			
			
		
		#return
		
		#j_items = []
		#for i in range(interactions_map.shape[0]):
			#if interactions_map[i][1] != j_items[len(j_items)-1]:
				#j_items.append(interactions_map[i][1])
		
		#print(j_items)
		
		
		#predicted_ratings = [] # take the 50 most similar!
		##for item in item_profiles:
			
			##similarity
				
			
			##predicted_ratings.append([ item, prediction ])
			
		##rec_matrix = []
		##rec_matrix.append([user, recommendations])
	
	return np.array([])





def writecsv(user_rec, target_users):
	
	###### WRITE SUBMISSION FILE ###################
	
	with open(SUBMISSION, 'wb') as csvfile:
		csvfile.write(bytes("user_id,recommended_items\n", 'UTF-8'))	
		for item in user_rec.itertuples():
			csvfile.write(bytes("{},{}\n".format(item[0], " ".join( str(item[1])[1:-1].split(', ')) ), 'UTF-8'))

	print(" # {} wrote successfully. Bye!".format(SUBMISSION))








################################################################################
################## OLD ALGS ####################################################
################################################################################


def recommendTopPop(interactions_map, item_profiles, user_profiles, target_users):

	#########  ALGORITHM - TopPop Refined  #########
	
	item_codes_statuses = item_profiles[['id', 'active_during_test']]
	# Keep only active items
	#item_codes_statuses = item_codes_statuses.loc[item_codes_statuses.active_during_test == 1]
	#print(item_codes_statuses.shape)
	
	# Selects the row of interacting items and the row of ratings
	interacting_items = interactions_map.drop('created_at', 1)
	#interacting_items = interacting_items.drop('x', 1)
	interacting_items = interacting_items.drop('user_id', 1)
	

	# Count each block and store the top frequencies
	top_popular = interacting_items.groupby('item_id').sum().sort(['interaction_type'], ascending=False)
	print("Top Pop: {}".format(top_popular.head()))
	top_popular = top_popular.index
	
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
	
	return rec_matrix
	
	
	
def recommendTopPopNP(interactions_map, item_profiles, user_profiles, target_users):

	#########  ALGORITHM - TopPop Refined  #########
	item_profiles = np.array(item_profiles)
	interactions_map = np.array(interactions_map)
	
	item_codes_statuses = np.column_stack( (item_profiles[:, 0], item_profiles[:, -1]) )
	# Keep only active items
	item_codes_statuses = item_codes_statuses[item_codes_statuses[:, 1] == 1]
	#print(interactions_map.shape)
	
	# Selects the row of interacting items and the row of ratings
	interacting_items = interactions_map[:,1:3]
	#print(interactions_map.shape)

	# Sort interactions table to generate "clusters"
	interacting_items = np.sort(interacting_items, axis=0)

	# Count each block and store the top five frequencies
	top_five = [[0, 0], [0,0], [0,0], [0,0], [0,0]]
	buffer_item = [0, 0]
	a = 0
	for i in range(interacting_items.shape[0]):
		a = i
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
	
	#recommendations = ""
	#for rec in top_five:
	#	recommendations += "{} ".format(rec[0])	
	recommendations = [r[0] for r in top_five]
	
	rec_matrix = []
	for user in target_users.iterrows():
		rec_matrix.append([ user[1][0], recommendations])
	
	#return zip(target_users, rec_matrix)
	
	# For the evaluator
	evaluable = pd.DataFrame( rec_matrix )
	evaluable = evaluable.rename(columns={0: 'user_id', 1: 'recs'})
	return evaluable
	
	
