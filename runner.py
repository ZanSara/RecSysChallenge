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
import traceback


# Constants
ROOT = "datasets/"
TRAINING_SET = "interactions_training.csv"
TESTING_LOCAL_SET = "interactions_testing.csv"
TESTING_FULL_SET = "interactions_full.csv"



def main():
    # Command-line parsing
    parser = OptionParser()
    parser.add_option("-f", "--test_full",
                      action="store_true", dest="full_test_set",
                      help="test the recommender on the full testing dataset.")
    parser.add_option("-l", "--test_local",
                      action="store_false", dest="full_test_set", default=False,
                      help="test the recommender on the local testing dataset (default behavior).")
    parser.add_option("-s", "--split-datasets",
                      action="store_true", dest="split", default=False,
                      help="takes the full dataset file has specified in the constants and split "+
                            "it into a reasonable couple of test-training datasets")


    (options, args) = parser.parse_args()

    # Split the dataset (una-tantum)
    if options.split:
        print(" # Loading interactions full dataset ({})...".format(TESTING_FULL_SET))
        interactions_map = sp.genfromtxt("{}{}".format(ROOT, TESTING_FULL_SET), dtype='int64', delimiter="\t", names=["users", "items", "inter", "date"])[1:]
        print("   -> got {} rows".format(interactions_map.shape[0]))
        print(" # Splitting datasets...")
        import dataset_splitter as s
        start = time.time()
        s.split(interactions_map)
        end = time.time()
        print(" # Done in {:3f} sec!".format(end-start))
        return

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
    print(" # Loading interactions full dataset ({})...".format(TESTING_FULL_SET))
    int_full_map = sp.genfromtxt("{}{}".format(ROOT, TESTING_FULL_SET), dtype='int64', delimiter="\t")[1:]
    print("   -> got {} rows".format(int_full_map.shape[0]))
    print(" # Loading interactions training dataset ({})...".format(TRAINING_SET))
    int_training_map = sp.genfromtxt("{}{}".format(ROOT, TRAINING_SET), dtype='int64', delimiter="\t")[1:]
    print("   -> got {} rows".format(int_training_map.shape[0]))
    print(" # Loading interactions test dataset ({})...".format(test_set))
    int_test_map = sp.genfromtxt("{}{}".format(ROOT, test_set), dtype='int64', delimiter="\t")[1:]
    print("   -> got {} rows".format(int_test_map.shape[0]))

    # Item Profiles' structure
    # id	title	career_level	discipline_id	industry_id	country	region	latitude	longitude	employment	tags	created_at	active_during_test
    print(" # Loading item profiles' dataset...")
    with open("{}item_profile.csv".format(ROOT), newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter='\t')
        item_profiles = np.array(list(csvreader))[1:]
    print("   -> got {} rows".format(item_profiles.shape[0]))

    # User Profiles' structure
    # user_id	jobroles	career_level	discipline_id	industry_id	country	region	experience_n_entries_class	experience_years_experience	experience_years_in_current	edu_degree	edu_fieldofstudies
    print(" # Loading user profiles' dataset...")
    user_profiles = sp.genfromtxt("{}user_profile.csv".format(ROOT), dtype='int64', delimiter="\t")[1:]
    print("   -> got {} rows".format(user_profiles.shape[0]))

    # Target users' structure
    # user_id
    print(" # Loading target users' dataset...")
    target_users = sp.genfromtxt("{}target_users.csv".format(ROOT), dtype='int64', delimiter="\t")[1:]
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
            r.recommend(int_training_map, int_test_map, int_full_map, item_profiles, user_profiles, target_users)
            end = time.time()
            
        # except Exception: CtrlC kills the runner too
        # except: CtrlC does NOT kill the runner at this stage
        except Exception:
            print("\n\n---> EXECUTION KILLED by an Exception:")
            print(traceback.format_exc())
            print("\n---------- EXECUTION COMPLETED WITH AN EXCEPTION ------------------".format(exec_number, end-start))
        except:
            end = time.time()
            print("\n\n---> EXECUTION KILLED (not by an Exception)")
            print("\n---------- EXECUTION INTERRUPTED at sec {:.3f} ------------------".format(end-start))
            end = 0
            
        if end != 0:
            print("\n---------- EXECUTION {} COMPLETED in {:.3f} sec --------------------".format(exec_number, end-start))
        print("--------------------------------------------------------------------\n\n")
        

    print("\nThe runner's exiting. Bye bye!")



if __name__ == "__main__":
    main()
