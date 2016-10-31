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
import pandas as pd
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
        #interactions_map = sp.genfromtxt("{}{}".format(ROOT, TRAINING_FULL_SET), dtype='int64', delimiter="\t", names=["users", "items", "inter", "date"])[1:]
        interactions_map =  pd.read_csv("{}{}".format(ROOT, TRAINING_FULL_SET), sep="\t")
        print("   -> got {} rows".format(interactions_map.shape[0]))
        print(" # Loading target users' table ...")
        #target_users = sp.genfromtxt("{}target_users.csv".format(ROOT), dtype='int64', delimiter="\t")[1:]
        target_users =  pd.read_csv("{}target_users.csv".format(ROOT), sep="\t")
        print("   -> got {} rows".format(target_users.shape[0]))
        
        import splitter2 as s
        print(" # Splitting datasets...")
        start = time.time()
        s.split(interactions_map, target_users)
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

    #### Interactions' structure
    #
    # user_id : ID of the user who performed the interaction 
    #            (points to users.id)
    # item_id : ID of the item on which the interaction was 
    #           performed (points to items.id)
    # interaction_type : the type of interaction that was performed 
    #                    on the item:
    #     1 = the user clicked on the item
    #     2 = the user bookmarked the item
    #     3 = the user clicked on the reply button or application 
    #         form button that is shown on some job postings
    # created_at : a unix time stamp timestamp representing the 
    #              time when the interaction got created
    print(" # Loading interactions' dataset...")
    int_training_map =  pd.read_csv("{}{}".format(ROOT, training_set), sep="\t")
    print("   -> got {} rows".format(int_training_map.shape[0]))
    
    # Load the test set only if I'm training on the local set
    int_test_map = []
    if training_set == TRAINING_LOCAL_SET:  
        print(" # Loading test dataset ({})...".format(TEST_SET))
        int_test_map = pd.read_csv("{}{}".format(ROOT, TEST_SET), sep="\t")
        print("   -> got {} rows".format(int_test_map.shape[0]))
        
    ### Item Profiles' structure
    #
    # id : anonymized ID of the item (item_id in interaction dataset)
    # title : concepts that have been extracted from the job title 
    #         of the job posting (numeric IDs)
    # career_level : career level ID (e.g. beginner, experienced, manager):
    #    0 = unknown
    #    1 = Student/Intern
    #    2 = Entry Level (Beginner)
    #    3 = Professional/Experienced
    #    4 = Manager (Manager/Supervisor)
    #    5 = Executive (VP, SVP, etc.)
    #    6 = Senior Executive (CEO, CFO, President)
    # discipline_id : anonymized IDs represent disciplines
    # industry_id : anonymized IDs represent industries
    # country : code of the country in which the job is offered
    # region : is specified for some users who have as country de.
    #           0 means not specified
    # latitude : latitude information (rounded to ca. 10km)
    # longitude : longitude information (rounded to ca. 10km)
    # employment : the type of employment:
    #    0 = unknown
    #    1 = full-time
    #    2 = part-time
    #    3 = freelancer
    #    4 = intern
    #    5 = voluntary
    # tags : concepts that have been extracted from the tags, skills 
    #        or company name
    # created_at : a Unix time stamp timestamp representing the time 
    #              when the interaction happened
    # active_during_test : is 1 if the item (job) is still active 
    #                      (= recommendable) during the test period and
    #                      0 if the item is not active anymore in the 
    #                      test period (= not recommendable)
    print(" # Loading item profiles' dataset...")
    item_profiles =  pd.read_csv("{}item_profile.csv".format(ROOT), sep="\t")
    print("   -> got {} rows".format(item_profiles.shape[0]))


    #### User Profiles' structure
    #
    # id : anonymized ID of the user (referenced as user_id in 
    #      the interaction dataset)
    # jobroles : comma-separated list of job role terms (numeric IDs)
    #            that were extracted from the user’s current job title. 
    #            0 means that there was no known jobrole detected for 
    #            the user.
    # career_level : career level ID (e.g. beginner, experienced, manager):
    #    0 = unknown
    #    1 = Student/Intern
    #    2 = Entry Level (Beginner)
    #    3 = Professional/Experienced
    #    4 = Manager (Manager/Supervisor)
    #    5 = Executive (VP, SVP, etc.)
    #    6 = Senior Executive (CEO, CFO, President)
    # discipline_id : anonymized IDs represent disciplines
    # industry_id : anonymized IDs represent industries
    # country : describes the country in which the user is now working:
    #    de = Germany
    #    at = Austria
    #    ch = Switzerland
    #    non_dach = non of the above countries
    # region : is specified for some users who have as country de. 
    #          0 means Not Specified
    # experience_n_entries_class : identifies the number of CV entries
    #                              the user has listed as work experiences:
    #    0 = no entries
    #    1 = 1-2 entries
    #    2 = 3-4 entries
    #    3 = 5 or more entries
    # experience_years_experience : number of years of work experience 
    #                               the user has:
    #    0 = unknown
    #    1 = less than 1 year
    #    2 = 1-3 years
    #    3 = 3-5 years
    #    4 = 5-10 years
    #    5 = 10-15 years
    #    6 = 16-20
    #    7 = more than 20 years
    # experience_years_in_current : number of years that the user is 
    #                               already working in her current job. 
    #           Meaning of numbers: same as experience_years_experience
    # edu_degree : university degree of the user:
    #    0 or NULL = unknown
    #    1 = bachelor
    #    2 = master
    #    3 = phd
    # edu_fieldofstudies : comma-separated fields of studies (anonymized
    #                      ids) that the user studied. 0 means “unknown”
    #                      and edu_fieldofstudies > 0 entries refer to 
    #                      broad field of studies
    print(" # Loading user profiles' dataset...")
    user_profiles = pd.read_csv("{}user_profile.csv".format(ROOT), sep="\t")
    print("   -> got {} rows".format(user_profiles.shape[0]))

    # Target users' structure
    # user_id
    print(" # Loading target users' dataset...")
    target_users = pd.read_csv("{}target_users.csv".format(ROOT), sep="\t")
    print("   -> got {} rows".format(target_users.shape[0]))

    end = time.time()

    print("\n---------- DATASETS LOADED IN {:.3f} sec -------------------------------------".format(end-start))
    print("------------------------------------------------------------------------------\n")



    ########  RUNNING LOOP ##################

    loaded = False
    while not loaded:
        try:
            import recommender as r
            import map_evaluator as e
            loaded = True
        except SyntaxError:
            print(traceback.format_exc())
            user_input = input("----> Press any key to retry...")
            
        
    exec_number = 0
    while True:
        user_input = input("\n # Press X to exit, F to load full datasets, L to load local datasets\n   or any other key to re-execute the recommender algorithm.\n")
        if user_input=="X" or user_input=="x":
            break
        if user_input=="F" or user_input=="f":
            training_set = TRAINING_FULL_SET
            int_training_map = pd.read_csv("{}{}".format(ROOT, training_set), sep="\t")
            continue
        if user_input=="L" or user_input=="l":
            training_set = TRAINING_LOCAL_SET
            int_training_map = pd.read_csv("{}{}".format(ROOT, training_set), sep="\t")
            continue
        
        try:
            il.reload(r)
            il.reload(e)
        except SyntaxError:
            print(traceback.format_exc())
            continue
        
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
                try:
                    e.evaluate(int_test_map, user_ratings)
                    
                except Exception:
                    print(traceback.format_exc())
                    print("\n-----> Evaluation gave exception")
            else:
                print("---> Writing Submission File")
                r.writecsv(user_ratings, target_users)
            
        print("--------------------------------------------------------------------\n\n")
        

    print("\nThe runner's exiting. Bye bye!")

    
    

if __name__ == "__main__":
    main()
