'''
Descripttion: 
version: 
Author: Roy White
Date: 2021-06-22 13:45:49
LastEditors: Roy White
LastEditTime: 2021-07-19 15:51:37
'''
import OTFasta as ot
import functions as func
import sys
from collections import Counter

# 统计输入fasta文件的kmers
def question_1():
    file_name = sys.argv[1] # input
    outfile = sys.argv[2] # output
    Fa = ot.Fasta(file_name)
    # merge seqs
    for seq_ in Fa.sequence:
        seq = ''.join(seq_.strip())
    # k
    for k in range(3, 20): # kmers 长度
        answer = {}
        kmers = func.gene_to_kmers(seq, k)
        kmers_fre = Counter(kmers).most_common(20)
        total_kmers = (len(seq)-k+1)
        expect_fre = 1/4**k
        for key, value in dict(kmers_fre).items():
            observe_fre = value/total_kmers
            enrich_score = observe_fre/expect_fre
            answer[key] = (value, "%.2f"%enrich_score)
        with open(outfile, 'a')as fw:
            fw.write(f'k={k}\t{answer}\n')