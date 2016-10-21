# -*- coding: utf-8 -*-

#######################################################
###                                                 ###
###                     RUNNER                      ###
###                                                 ###
###  Utility platform that load datasets only once  ###
###  and re-executes the updated recommender script ###
###  multiple times, as the user wishes.            ###
###                                                 ###
#######################################################

from optparse import OptionParser
import time
import scipy as sp
import numpy as np
import csv
import importlib as il


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
    print("\n # FULL dataset chosen for testing")
else:
    test_set = TESTING_LOCAL_SET
    print("\n # LOCAL dataset chosen for testing")
    
    
    
    

######## LOADING DATASETS ########

print("\n-----------------------------------------------------------------")
print("---------- LOADING DATASETS -------------------------------------\n")

start = time.time()

# Interactions' structure
# user_id	item_id		interaction_type	created_at
print(" # Loading interactions dataset...")
interactions_map = sp.genfromtxt("{}interactions.csv".format(test_set), dtype='int64', delimiter="\t")
print("   -> got {} rows".format(interactions_map.shape[0]))

# Item Profiles' structure
# id	title	career_level	discipline_id	industry_id	country	region	latitude	longitude	employment	tags	created_at	active_during_test
print(" # Loading item profiles' dataset...")
with open("{}item_profile.csv".format(test_set), newline='') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t')
    item_profiles = np.array(list(csvreader))
print("   -> got {} rows".format(item_profiles.shape[0]))

# User Profiles' structure
# user_id	jobroles	career_level	discipline_id	industry_id	country	region	experience_n_entries_class	experience_years_experience	experience_years_in_current	edu_degree	edu_fieldofstudies
print(" # Loading user profiles' dataset...")
user_profiles = sp.genfromtxt("{}user_profile.csv".format(test_set), dtype='int64', delimiter="\t")
print("   -> got {} rows".format(user_profiles.shape[0]))

# Target users' structure
# user_id
print(" # Loading target users' dataset...")
target_users = sp.genfromtxt("{}target_users.csv".format(test_set), dtype='int64', delimiter="\t")
print("   -> got {} rows".format(target_users.shape[0]))

end = time.time()

print("\n---------- DATASETS LOADED IN {:.3f} sec -------------------------------------".format(end-start))
print("------------------------------------------------------------------------------\n")



########  RUNNING LOOP ##################

import recommender as r
exec_number = 0
while True:
    user_input = input("\n # Press X to exit, or any other key to re-execute the recommender algorithm.\n")
    if user_input=="X" or user_input=="x":
        break
        
    il.reload(r)
    exec_number += 1
    start = 0
    end = 0
    print("\n--------------------------------------------------------------------".format(end-start))
    print("---------- START EXECUTION {} -------------------------------------\n".format(exec_number))
    try:
        start = time.time()
        r.recommend(interactions_map, item_profiles, user_profiles, target_users)
        end = time.time()
    # except Exception: CtrlC kills the runner too
    # except: CtrlC does NOT kill the runner at this stage
    except:
        print("\n\n---> EXECUTION KILLED (by an Exception or a KeyboardInterrupt)")
        
    if end == 0:
        print("\n---------- EXECUTION COMPLETED WITH AN EXCEPTION ------------------".format(exec_number, end-start))
    else:
        print("\n---------- EXECUTION {} COMPLETED in {:.3f} sec --------------------".format(exec_number, end-start))
    print("--------------------------------------------------------------------\n\n")
    

print("\nThe runner's exiting. Bye bye!")



