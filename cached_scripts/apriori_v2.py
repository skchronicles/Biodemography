########################################################################################################################
# Skyler Kuhn and Hasan Alkhairo
# Center for the Study of Biological Complexity
# Biodemography Project: Apriori Algorithm
# Version 1.2
########################################################################################################################
from __future__ import print_function


def preprocess(q, q_pvalue):
    insig = []
    for num in q:
        if q_pvalue[tuple([num])] == 0:
            q.remove(num)
            insig.append(num)
    return q, insig


def apriori(q, q_pvalues, insig):
    """ This function implements a modified version of the apriori algorithm which can be used for speeding up
    an otherwise exhaustive high-performance computing problem. The apriori algorithm is commonly used in mining
    frequent itemsets for boolean association rules. It uses a monotonic "bottom up" approach, where frequent subsets
    are extended one item at a time. """

    insignificant = [] + insig
    significant = []

    while len(q) > 0:
        element = q[0]
        if isinstance(element, int):
            element = tuple([element]) # it easier to just convert this to a tuple (so everything is the same data type)

        pvalue = q_pvalues[element]   # chi-squared test, verify if the given element satisfies the support criterion

        if pvalue == 1:
            significant.append(element)
            #print significant
            for i in range(element[-1]+1,4):
                if i not in insignificant:
                    #print i, "#####", element
                    tentativeCandidate = tuple(sorted(list(element)+[i])) # add the two lists together (element is a list)
                    if tentativeCandidate not in q and tentativeCandidate not in significant: # then add it to the queue
                        #print "Queue {}\nTentative Candidate{}\nSignificant {}\nInsignicant {}\n" \
                        #      "##################################".format(q,tentativeCandidate,significant,insignificant)
                        q.append(tentativeCandidate)
                        yield q,tentativeCandidate,significant,insignificant
            q.pop(0) #remove it from the queue after we have created/tried all the tentativeCandidates

        else:        # when the p-value not significant
            q.pop(0)
            insignificant.append(element)
            yield q,tentativeCandidate,significant,insignificant
    else:
        yield q,tentativeCandidate,significant,insignificant  # grab the last values before breaking out of the while loop

if __name__ == "__main__":
    qu = [1,2,3]
    q_pvalues = {(1,):1,(2,):1,(3,):1,(1,2):1,(1,3):1,(2,3):1,(1,2,3):1} # look into a list of dictionaries, testing with all significant values
    qu, insig = preprocess(qu, q_pvalues)
    #print "This is the queue after intial pre-processing", q
    for q, tentativeCandidate, significant, insignificant in apriori(qu,q_pvalues, insig):
        print("Queue {}\nTentative Candidate{}\nSignificant {}\nInsignicant {}\n" \
                              "##################################".format(q,tentativeCandidate,significant,insignificant))
