#####################################################
# Skyler Kuhn & Hasan Alkhairo
# Biodemography Analysis
# Center for the Study of Biological Complexity
# Version 1.2
#####################################################

from __future__ import print_function, division
from scipy.stats import chi2_contingency, chisquare, contingency
import numpy as np


def chi_square_analysis(obs_list):
    """Had to change interpreter from Python 3.5 to 2.7 (located in /usr/bin/python)"""
    obs = np.array(obs_list)
    chi2, p, dof, expected = chi2_contingency(obs)
    return chi2, p, dof, expected



if __name__== "__main__":

    chisq, pvalue = chisquare([1567, 1500, 1599, 1643, 1573])
    #expected = [100000, 60000, 50000, 15000, 35000]
    #observed = [16, 18, 16, 14, 12, 12]
    #expected = [sum(observed)/ len(observed) for i in observed]  # not neccessary

    print("Chi-squared test statistic: {}\t |\tp-value: {}".format(chisq, pvalue))
