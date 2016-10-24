
###################################################################
#                                                                 #
#                          EVALUATOR                              #
#                                                                 #
#  The average precision at 5, for a user is defined as:          #
#                                                                 #
#               AP@5  =  ∑(k=1-5) P(k) / min(m,5)                 #
#                                                                 #
#  where P(k) means the precision at cut-off k in the item list   #
#  and m is the n. of relevant items in the list. P(k) equals 0   #
#  if k -th item is not relevant. If the denominator is 0, the    #
#  result is set 0.                                               #
#                                                                 #
#  The mean average precision for N users at position 5 is the    #
#  average of the average precision of each user, i.e.            #
#                                                                 #
#                  MAP@5  =  ∑(i=1-N) AP@5_i / N                  #
#                                                                 #
###################################################################





def evaluate(relevant, user_ratings):
    
    sum_ap = 0
    for user in user_ratings:
        recom = set(user_ratings.split())
        for i in range(recom.size(), -1, -1):
            if 
            
    
    mapval = 0
    
    print(" # MAP@5 value: {:.7f}".format( mapval ))
