# -*- coding: utf-8 -*-

# Fundamental imports
import numpy as np
import scipy as sp
import pandas as pd

# Utility imports
from optparse import OptionParser
import csv

# Constants
ROOT = "datasets/"
TRAINING_SET = "interactions_training.csv"
TEST_SET = "interactions_testing.csv"


def split(interactions_map, target_users):
    
    # "If you want to build a local test set, taking the 5 last interactions
    # of the users may be a good approximation of what we did."

    ###### SPLITTING ALGORITHM ###################
    
	# Sort interactions table to generate "clusters" of users
    # and items - should also shuffle by date!
    sorted_interactions = interactions_map.sort(['user_id', 'item_id'])
    print(sorted_interactions.head())
    
	# For each block move the first five elements in the test set  
    # matrix, the rest of them in the training set matrix
    test_set = pd.DataFrame(columns=['user_id', 'recs'])
    training_set = pd.DataFrame(columns= sorted_interactions.columns )
    print("Test_set\n {}".format(test_set.head()))
    print("Training_set\n {}".format(training_set.head()))
    
    buffer_item = 0
    buffer_user = 0
    counting = 1
    test = 0
    for element in sorted_interactions.iterrows():
        
        if element[0] != buffer_user:
            counting = 1
            buffer_user = element[0]
            buffer_item = element[1]
            test_set = test_set.append( list(element), ignore_index=True)
            if test<10:
                test+=1
                print("###########")
                print(element.__class__)
                print(list(element))
                print("------")
                print(test_set)
        else:
            if counting < 5 or element[1] == buffer_item:
                test_set = test_set.loc[test_set['user_id'] == buffer_user].append( pd.Series(element), ignore_index=True )
                if element[1] != buffer_item:
                    counting += 1
                    buffer_item = element[1]
            else:
                training_set = training_set.append( pd.Series(element), ignore_index=True)
                
    test_npset = np.array(test_set)
    training_npset = np.array(training_set)
    
    print("Results:")
    print(test_npset[:10])
    print(training_npset[:10])
    return
    
    
    ######## FORMAT THE TEST SET IN USER-RECS FORMAT ################
    
    # Build the table of recommendations
    relevants = pd.DataFrame(columns=['user_id', 'recs'], index=target_users)
    buffer_user = 0
    buffer_item = 0
    last_row = -1
    last_rec = 1
    for element in test_npset:
        if element[0] == buffer_user:
            if element[1] != buffer_item:
                last_rec += 1
                buffer_item = element[1]
                relevants.iloc[last_row]['recs'].append(element[1])
        else:
            if element[0] in target_users:
                last_row +=1
                buffer_user = element[0]
                relevants.iloc[last_row]['user_id'] = element[0]
                last_rec = 1
                buffer_item = element[1]
                relevants.iloc[last_row]['recs'] = [element[1]]
    
    # Add all target users that had no recommendations in test_npset
    for user in target_users:
        if not user in relevants['user_id']:
            relevants.iloc[last_row]['user_id'] = user
            last_row += 1
    
    sorted_relevants = relevants.sort('user_id')
    sorted_relevants = sorted_relevants.set_index('user_id')
    print(sorted_relevants.head())
            
    
    ###### WRITE DATASETS FILES ###################
    
    print("Writing stuff")
    print(training_npset)
    training = pd.DataFrame(training_npset)
    print(training.head(10))
    training.set_index('user_id')
    training.to_csv("{}{}".format(ROOT, TRAINING_SET), sep='\t')
    print(" -> {} ({:.1f}% of full dataset) wrote successfully".format(TRAINING_SET, training_npset.shape[0]*100/sorted_interactions.shape[0]))
    
    sorted_relevants.to_csv("{}{}".format(ROOT, TEST_SET), sep='\t')
    print(" -> {} ({:.1f}% of full dataset) wrote successfully".format(TEST_SET, test_npset.shape[0]*100/sorted_interactions.shape[0] ))
    
    
    #with open("{}{}".format(ROOT, TRAINING_SET), 'wb') as csvfile:
        #csvfile.write(bytes("user_id\titem_id\tinteraction_type\tcreated_at\n", 'UTF-8'))    
        #for row in training_npset:
            #string = ""
            #for field in row:
                #string += "{}\t".format(field)
            #csvfile.write(bytes("{}\n".format(string.rstrip()), 'UTF-8'))
    #print(" -> {} ({:.1f}% of full dataset) wrote successfully".format(TRAINING_SET, training_npset.shape[0]*100/sorted_interactions.shape[0]))

    #with open("{}{}".format(ROOT, TEST_SET), 'wb') as csvfile:
        #csvfile.write(bytes("user_id\trec1\trec2\trec3\trec4\trec5\n", 'UTF-8'))	
        #for row in sorted_relevants:
            #string = ""
            #for field in row:
                #string += "{}\t".format(field)
            #csvfile.write(bytes("{}\n".format(string.rstrip()), 'UTF-8'))
    #print(" -> {} ({:.1f}% of full dataset) wrote successfully".format(TEST_SET, test_npset.shape[0]*100/sorted_interactions.shape[0] ))
    
