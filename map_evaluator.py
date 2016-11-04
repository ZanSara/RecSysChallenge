
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

COUNTER = 0


def evaluate(relevant_items, user_ratings, k=5):
    
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
   
    # Load previous value of MAP@5
    with open("evaluations.txt") as f:
        cache = f.readlines()
        old_mapval = float(cache[-1])
        
    # Calculate MAP@5
    print(relevant_items.head())
    print(user_ratings.head())
    
    mapval = np.mean([apk(a,p,k) for a,p in zip(relevant_items.recs, user_ratings.recs)])
    
    # Comparisons
    print("     # MAP@5 = {:.5f}".format(mapval))
    if mapval == old_mapval:
        print("       No difference over the last run.")
    else:
        if mapval > old_mapval:
            print("       MAP IMPROVED over the last run! Difference is {:.5f} (previous evaluation: {:.5f})".format(mapval-old_mapval, old_mapval))
        else:
            print("       MAP GOT WORSE over the last run! Difference is -{:.5f} (previous evaluation: {:.5f})".format(old_mapval-mapval, old_mapval))
        
        # Saves calculated data into evaluations.txt
        cache.append('{}\n'.format(mapval))
        with open("evaluations.txt", 'wb') as f:
            for line in cache:
                f.write(bytes('{}'.format(line), 'UTF-8'))	
            
                

def apk(actual, predicted, k=5):
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
    
    actual = [ (int(x) if x!='' else 0) for x in actual[1:-1].split(', ')]   # Actuals are in form [1, 2, 3] and need to be changed into ints
    #predicted = predicted.split()    # Predicted are in form '1 2 3' -> No more!
    
    #print('actual: {}\npredicted: {} '.format(actual, predicted))
    if not actual:
        return 0.0
        
    if len(predicted)>k:
        predicted = predicted[:k]

    score = 0.0
    num_hits = 0.0

    for i,p in enumerate(predicted):
        if p in actual and p not in predicted[:i]:
            num_hits += 1.0
            score += num_hits / (i+1.0)

    return score / min(len(actual), k)








# EX CODE FOR NEW_RELEVANT DATASET
def make_new_relevant(relevant_items, user_ratings):
    new_relevant = pd.DataFrame(columns=['recs'], index=relevant_items.user_id)
    print(new_relevant.head())
    for i in range(new_relevant.shape[0]):
        buffer_list = [x for x in relevant_items.iloc[i][1:]]
        new_relevant.iloc[i].recs = buffer_list[0]
    
    print(new_relevant.info())
    new_relevant.to_csv("{}new_relevants.csv".format(ROOT), sep='\t')
    print("Now returning!")
