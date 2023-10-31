'''
Descripttion: 
version: 
Author: Roy White
Date: 2021-07-12 19:51:24
LastEditors: Please set LastEditors
LastEditTime: 2021-09-14 17:37:51
'''

from scipy import stats
import numpy as np

def check_hypothesis(statistic, alpha=0.05):
    if statistic > alpha: # possiblity of error type 1
        return True # accept original hypothesis
    else:
        return False # refuse original hypothesis

def norm_test(list1):
    return check_hypothesis(stats.kstest(list1, 'norm').pvalue)

def f_test(data1, data2, alpha = 0.05): # Original hypothesis: No significant difference
    brt = stats.bartlett(data1, data2)
    lvn = stats.levene(data1, data2)
    return(check_hypothesis(brt.pvalue, alpha) and check_hypothesis(lvn.pvalue, alpha))

def t_test(data1, data2, rel = False, alpha=0.05):
    if rel: # paired t-test
        t = stats.ttest_rel(data1, data2)
        return check_hypothesis(t.pvalue, alpha), t.pvalue
    else:
        if f_test(data1, data2): # Homogeneity of variance
            t = stats.ttest_ind(data1, data2)
            return check_hypothesis(t.pvalue, alpha), t.pvalue
        else: # Inhomogeneity of variance
            t = stats.ttest_ind(data1, data2, equal_var=False)
            return check_hypothesis(t.pvalue, alpha), t.pvalue


def mann_whitneyu_test(list1, list2):
    return stats.mannwhitneyu(list1, list2)


def rank_sums_test(list1, list2): # Wilcoxon
    return stats.ranksums(list1, list2)


if __name__=='__main__':
    data1 = (2.4,10,3.35,24.5,20.5,10.5,19.5,29.5,6,21.75,14.875,15,19.5,25,10.5,19.75,11.75,18.16666667,17.5,10.5,9.75,17.875,16,21.5,11.4,12,21,12,13.5)
    data2 = (3,9.05,16.9,19,22.5,10.5,18.5,28.5,25,24,1.5,22,10,20.25,17.5,24.5,17.5,14.66666667,17,2.833333333,20.5,23,14.25,15,17.375,17.5)
    print(f_test(data1, data2))
    print(norm_test(data1), norm_test(data2))
    print(rank_sums_test(data1,data2))
    print(t_test(data1,data2))