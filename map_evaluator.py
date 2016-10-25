
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


def evaluate(relevant_items, user_ratings):
    
    # Load previous value of MAP@5
    with open("evaluations.txt") as f:
        old_mapval = float(f.readlines()[-1])
    
    
    # I assume both relevant_items and user_rating contain THE SAME USERS IN
    # THE SAME ORDER, so that:  user_ratings[i][0] == relevant_items[i][0]
    # always hold
    
    test = 0
    sum_ap = 0
    for i in range(user_ratings.shape[0]):
        ap = 0
        recom = [int(x) for x in user_ratings[i][1].split()] # converte la lista di stringhe in lista di int
        if int(user_ratings[i][0]) != relevant_items[i][0]:
            print("ERRORE! user_ratings[i][0] != relevant_items[i][0] : {} vs {}".format(user_ratings[i][0], relevant_items[i][0]))
            return 0
            
        relevants_given = [x for x in relevant_items[i, 1:] if x!=0]
        n_rel_given = len(relevants_given)
        
        #if test<10:
            #print("n_rel_given: {}".format(n_rel_given))
        if n_rel_given != 0:

            m_relevant_items_found = 0
            for k in range(5):
                if recom[k] in relevants_given:
                    m_relevant_items_found +=1
                    ap += m_relevant_items_found/(k+1)
            sum_ap += ap/ min(k+1, n_rel_given)
            
            if test < 10 and ap !=0:
                test += 1
                #print("{}  -> {}".format(relevants_given, ap/n_rel_given))
    
    
    mapval = sum_ap/relevant_items.shape[0]
    
    # Saves calculated data into evaluations.txt
    if mapval != old_mapval:
        with open("evaluations.txt", 'wb') as f:
            f.write(bytes("{}\n".format(mapval), 'UTF-8'))	
    
    print("     # MAP@5 = {:.5f}".format(mapval))
    if mapval == old_mapval:
        print("       No difference over the last run.")
    else:
        if mapval > old_mapval:
            print("       MAP IMPROVED over the last run! Difference is {:.5f} (previous evaluation: {:.5f})".format(mapval-old_mapval, old_mapval))
        else:
            print("       MAP GOT WORSE over the last run! Difference is -{:.5f} (previous evaluation: {:.5f})".format(old_mapval-mapval, old_mapval))
    
    
