# -*- coding: utf-8 -*-

########################################################
###                                                  ###
###                     RUNNER                       ###
###                                                  ###
###  Utility platform that load datasets only once   ###
###  and re-executes the updated recommender script  ###
###  multiple times, as the user wishes.             ###
###                                                  ###
########################################################

from optparse import OptionParser
import time
import scipy as sp
import numpy as np
import csv
import importlib as il
import traceback


# Constants
ROOT = "datasets/"
TEST_SET = "interactions_testing.csv"
TRAINING_LOCAL_SET = "interactions_training.csv"
TRAINING_FULL_SET = "interactions_full.csv"



def main():
    # Command-line parsing
    parser = OptionParser()
    parser.add_option("-f", "--test_full",
                      action="store_true", dest="full_training_set",
                      help="test the recommender on the full training dataset.")
    parser.add_option("-l", "--test_local",
                      action="store_false", dest="full_training_set", default=False,
                      help="test the recommender on the local training dataset (default behavior).")
    parser.add_option("-s", "--split-datasets",
                      action="store_true", dest="split", default=False,
                      help="takes the full dataset file has specified in the constants and split "+
                            "it into a reasonable couple of test-training datasets")


    (options, args) = parser.parse_args()

    # Split the dataset (una-tantum)
    if options.split:
        print(" # Loading interactions full dataset ({})...".format(TRAINING_FULL_SET))
        interactions_map = sp.genfromtxt("{}{}".format(ROOT, TRAINING_FULL_SET), dtype='int64', delimiter="\t", names=["users", "items", "inter", "date"])[1:]
        print("   -> got {} rows".format(interactions_map.shape[0]))
        print(" # Splitting datasets...")
        import dataset_splitter as s
        start = time.time()
        s.split(interactions_map)
        end = time.time()
        print(" # Done in {:3f} sec!".format(end-start))
        return

    if options.full_training_set:
        training_set = TRAINING_FULL_SET
        print("\n # FULL dataset chosen for training")
    else:
        training_set = TRAINING_LOCAL_SET
        print("\n # LOCAL dataset chosen for training")
        
        

        
        

    ######## LOADING DATASETS ########

    print("\n-----------------------------------------------------------------")
    print("---------- LOADING DATASETS -------------------------------------\n")

    start = time.time()

    # Interactions' structure
    # user_id	item_id		interaction_type	created_at
    int_training_map = load_int(training_set, "training")
    
    # Load the test set only if i'm training on the local set
    int_test_map = []
    if training_set == TRAINING_LOCAL_SET:  
        int_test_map = load_int(TEST_SET, "test")
        
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
    import map_evaluator as e
    exec_number = 0
    while True:
        user_input = input("\n # Press X to exit, F to load full datasets, L to load local datasets\n   or any other key to re-execute the recommender algorithm.\n")
        if user_input=="X" or user_input=="x":
            break
        if user_input=="F" or user_input=="f":
            training_set = TRAINING_FULL_SET
            int_training_map = load_int(training_set, "training full")
            continue
        if user_input=="L" or user_input=="l":
            training_set = TRAINING_LOCAL_SET
            int_training_map = load_int(training_set, "training local")
            continue
            
        il.reload(r)
        il.reload(e)
        exec_number += 1
        start = 0
        end = 0
        print("\n--------------------------------------------------------------------".format(end-start))
        print("---------- START EXECUTION {} -------------------------------------\n".format(exec_number))
        try:
            start = time.time()
            user_ratings = r.recommend(int_training_map, item_profiles, user_profiles, target_users)
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

            # Do evaluate if I have a test_set to evaluate on
            if training_set == TRAINING_LOCAL_SET:  
                print("---> Evaluation:")
                e.evaluate(int_test_map, user_ratings)
            else:
                print("---> Writing Submission File")
                r.writecsv(user_ratings, target_users)
            
        print("--------------------------------------------------------------------\n\n")
        

    print("\nThe runner's exiting. Bye bye!")




# Load a specific interactions dataset
def load_int(int_file, name):
    print(" # Loading interactions {} dataset ({})...".format(name, int_file))
    interactions = sp.genfromtxt("{}{}".format(ROOT, int_file), dtype='int64', delimiter="\t")[1:]
    print("   -> got {} rows".format(interactions.shape[0]))
    return interactions
    
    

if __name__ == "__main__":
    main()
