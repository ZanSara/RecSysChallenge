# -*- coding: utf-8 -*-

# Fundamental imports
import numpy as np
import scipy as sp

# Utility imports
from optparse import OptionParser
import csv

# Constants
ROOT = "datasets/"
TRAINING_SET = "interactions_training.csv"
TEST_SET = "interactions_testing.csv"


def split(interactions_map):
    
    # "If you want to build a local test set, taking the 5 last interactions
    # of the users may be a good approximation of what we did."

    ###### SPLITTING ALGORITHM ###################
    
	# Sort interactions table to generate "clusters" of users
    # and items - should also shuffle by date!
    ind = np.lexsort((interactions_map["items"], interactions_map["users"]))
    sorted_interactions = interactions_map[ind]
    
    print(sorted_interactions[:20])
   
	# For each block move the first five elements in the test set  
    # matrix, the rest of them in the training set matrix
    test_set = []
    training_set = []
    buffer_item = 0
    buffer_user = 0
    counting = 1
    for element in sorted_interactions:
        
        if element[0] == buffer_user:
            if counting < 5 or element[1] == buffer_item:
                test_set.append( element )
                if element[1] != buffer_item:
                    counting += 1
                    buffer_item = element[1]
            else:
                training_set.append( element )
        else:
            counting = 1
            buffer_user = element[0]
            buffer_item = element[1]
            test_set.append( element )

    test_npset = np.array(test_set)
    training_npset = np.array(training_set)
    
    
    ###### WRITE DATASETS FILES ###################
    
    with open("{}{}".format(ROOT, TEST_SET), 'wb') as csvfile:
        csvfile.write(bytes("user_id\titem_id\tinteraction_type\tcreated_at\n", 'UTF-8'))	
        for row in test_npset:
            string = ""
            for field in row:
                string += "{}\t".format(field)
            csvfile.write(bytes("{}\n".format(string.rstrip()), 'UTF-8'))
    print(" -> {} ({} rows, {:.1f}% of full dataset) wrote successfully".format(TEST_SET, test_npset.shape[0], test_npset.shape[0]*100/sorted_interactions.shape[0] ))
    
    
    with open("{}{}".format(ROOT, TRAINING_SET), 'wb') as csvfile:
        csvfile.write(bytes("user_id\titem_id\tinteraction_type\tcreated_at\n", 'UTF-8'))    
        for row in training_npset:
            string = ""
            for field in row:
                string += "{}\t".format(field)
            csvfile.write(bytes("{}\n".format(string.rstrip()), 'UTF-8'))
    print(" -> {} ({} rows, {:.1f}% of full dataset) wrote successfully".format(TRAINING_SET, training_npset.shape[0], training_npset.shape[0]*100/sorted_interactions.shape[0]))
