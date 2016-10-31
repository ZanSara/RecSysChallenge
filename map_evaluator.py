
###################################################################
#                                                                 #
#                          EVALUATOR                              #
#                                                                 #
#  The average precision at 5, for a user is defined as:          #
#                                                                 #
#               AP@5  =  ∑(k=1-5) P(k) / min(m,5)                 #
#                                                                 #
#  where P(k) means the precision at cut-off k in the item list   #
#  i.e., the ratio of number of relevant recommendations up to    #
#  the position k, over the number k, and m is the number of      #
#  relevant items in the list. P(k) equals 0 if k-th item is not  #
#  relevant. If the denominator is 0, the result is set 0.        #
#                                                                 #
#     "Precision at i is a percentage of correct items among      #
#                    first i recommendations."                    #
#                                                                 #
#  The mean average precision for N users at position 5 is the    #
#  average of the average precision of each user, i.e.            #
#                                                                 #
#                  MAP@5  =  ∑(i=1-N) AP@5_i / N                  #
#                                                                 #
###################################################################


import numpy as np
import pandas as pd
ROOT = "datasets/"


def evaluate(relevant_items, user_ratings):
    
    #return evaluateMAP(relevant_items, user_ratings)
    ####################################################################
    
    # Load previous value of MAP@5
    with open("evaluations.txt") as f:
        old_mapval = float(f.readlines()[-1])

    # I assume both relevant_items and user_rating contain THE SAME USERS IN
    # THE SAME ORDER, so that:  user_ratings[i][0] == relevant_items[i][0]
    # always hold
    
    relevant_items = relevant_items.set_index('user_id')
    
    test = 0
    sum_ap = 0
    for i in user_ratings.index:
        ap = 0
            
        if not i in relevant_items.index:
            #print("This has no relevant items! {}".format(i))
            continue
            
        if user_ratings.loc[i].index != relevant_items.loc[i].index:
            print("ERRORE! user_ratings[i][0] != relevant_items[i][0] : {} vs {}".format(user_ratings.loc[i], relevant_items.loc[i]))
            return 0
            
        r_given = relevant_items.loc[i].recs
        relevants_given = r_given[1:-2].split(",")
        n_rel_given = len(relevants_given)
        if test<5:
            test+=1
            print(relevants_given)
        
        if n_rel_given != 0:
            m_relevant_items_found = 0
            for k in range(len(user_ratings.loc[i].recs)):
                predicted_recom = (user_ratings.loc[i].recs)[k]
                if test<5:
                    print(predicted_recom)
                if predicted_recom in relevants_given:
                    if test<5:
                        print("matched!")
                    m_relevant_items_found +=1
                    ap += m_relevant_items_found/(k+1)
            sum_ap += ap/ min(k+1, n_rel_given)
            
            if test < 5 and ap !=0:
                print("{}  -> {}".format(relevants_given, ap/n_rel_given))
    
    
    mapval = sum_ap/relevant_items.shape[0]
    
    # Saves calculated data into evaluations.txt
    #if mapval != old_mapval:
        #with open("evaluations.txt", 'wb') as f:
            #f.write(bytes("{}\n".format(mapval), 'UTF-8'))	
    
    print("     # MAP@5 = {:.5f}".format(mapval))
    if mapval == old_mapval:
        print("       No difference over the last run.")
    else:
        if mapval > old_mapval:
            print("       MAP IMPROVED over the last run! Difference is {:.5f} (previous evaluation: {:.5f})".format(mapval-old_mapval, old_mapval))
        else:
            print("       MAP GOT WORSE over the last run! Difference is -{:.5f} (previous evaluation: {:.5f})".format(old_mapval-mapval, old_mapval))
    
    
    
    
    
    
    
    
    
    
def evaluateMAP(relevant_items, user_ratings):
    print(relevant_items.head())
    print(user_ratings.head())
    
    print("     # MAP@5 = {:.5f}".format(  mapk(relevant_items, user_ratings )  ))
    
  

def apk(actual, predicted, k=10):
    """
    Computes the average precision at k.

    This function computes the average prescision at k between two lists of
    items.

    Parameters
    ----------
    actual : list
             A list of elements that are to be predicted (order doesn't matter)
    predicted : list
                A list of predicted elements (order does matter)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The average precision at k over the input lists

    """
    
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    if not actual:
        return 0.0

    return score / min(len(actual), k)

def mapk(actual, predicted, k=10):
    """
    Computes the mean average precision at k.

    This function computes the mean average prescision at k between two lists
    of lists of items.

    Parameters
    ----------
    actual : list
             A list of lists of elements that are to be predicted 
             (order doesn't matter in the lists)
    predicted : list
                A list of lists of predicted elements
                (order matters in the lists)
    k : int, optional
        The maximum number of predicted elements

    Returns
    -------
    score : double
            The mean average precision at k over the input lists

    """
    print("MAPK")
    print(actual.head())
    print(predicted)
    
    return np.mean([apk(a,p,k) for a,p in zip(actual, predicted)])








# EX CODE FOR NEW_RELEVANT DATASET
def make_new_relevant():
    new_relevant = pd.DataFrame(columns=['recs'], index=relevant_items.user_id)
    print(new_relevant.head())
    for i in range(new_relevant.shape[0]):
        buffer_list = [x for x in relevant_items.iloc[i][1:]]
        new_relevant.iloc[i].recs = buffer_list[0]
    
    print(new_relevant.head())
    new_relevant.to_csv("{}new_relevants.csv".format(ROOT), sep='\t')
    print("Now returning!")
