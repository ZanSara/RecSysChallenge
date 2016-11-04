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
    
    test_set = pd.DataFrame( index=target_users.user_id, columns=['recs'])
    training_set = pd.DataFrame( index=interactions_map.index, columns= sorted_interactions.columns )
    
    print(test_set.head())
    
    buffer_item = 0
    buffer_user = 0
    buffer_list = []
    how_many_in_buffer = 1
    #test_row = -1
    training_row = 0
    test = 0
    
    try:
        start = time.time()
        a = 0
        for i, row in enumerate(sorted_interactions.iterrows()):
            
            element = sorted_interactions.iloc[i]
            a = i
            
            if element[0] != buffer_user:
                test_set.loc[buffer_user, 'recs'] = buffer_list
                #test_row +=1
                #test_set.loc[buffer_user].user_id = element[0]
                buffer_list = []
                how_many_in_buffer = 0
                buffer_user = element[0]
                buffer_item = element[1]
            else:
                if how_many_in_buffer < 5 and element[1] != buffer_item:
                    how_many_in_buffer += 1
                    buffer_item = element[1]
                    buffer_list.append(element[1])
                else:
                    training_set.iloc[training_row].user_id = element[0]
                    training_set.iloc[training_row].item_id = element[1]
                    training_set.iloc[training_row].interaction_type = element[2]
                    training_set.iloc[training_row].created_at = element[3]
                    training_row +=1
    except KeyboardInterrupt:
        end = time.time()
        print(" Elapsed: {:.5f} sec. to reach {:.3f}% of sorted_interactions".format(end-start, i/sorted_interactions.shape[0]))
        print("test set:")
        print(test_set.head(20))
        print("training set:")
        print(training_set.head(20))
        return
    except:
        print("Exception!")
        print(traceback.format_exc())
        print(test_row)
        print(test_set.info())
        print(buffer_user)
        print(test_set.head())
        print(test_set.tail())
        return
        
    #test_npset = np.array(test_set)
    #training_npset = np.array(training_set)
    
    # Fixing the test set from its NaN
    test_set = test_set.recs.fillna('[]')
    
    # Fixing the size of the training set
    training_set = training_set.head(training_row+1)
    
    print("Results:")
    print(test_set[:20])
    print(training_set[:20])


    ###### WRITE DATASETS FILES ###################
    
    print("\n\n # Writing stuff")
    training_set.to_csv("{}{}".format(ROOT, TRAINING_SET), sep='\t')
    print(" -> {} ({:.1f}% of full dataset) wrote successfully".format(TRAINING_SET, training_set.shape[0]*100/sorted_interactions.shape[0]))
    
    test_set.to_csv("{}{}".format(ROOT, TEST_SET), sep='\t')
    print(" -> {} wrote successfully".format(TEST_SET) )
    
