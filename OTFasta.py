'''
Description: Analysis fasta, return pandas dataframe
====================================function list=============================================

version: 
Author: Roy White
Date: 2021-05-20 13:08:43
LastEditors: Please set LastEditors
LastEditTime: 2021-11-18 20:56:32
'''

import re

import numpy as np
import pandas as pd
from pandas.core.accessor import DirNamesMixin

class Fasta():
    def __init__(self, file_name:str) -> None:
        '''
        @discription: transfer fasta to dataframe
        '''        
        self.file = file_name # fasta file name
        self.lines = [] # fasta file lines
        self.count = '' # seq number
        # dataframe features
        self.gene_id = [] # gene name(simplify) list
        self.transcript_name = [] # transcript name list
        self.sequence = [] # seq list
        self.seq_len = [] # seq len list
        self.GC_rate = [] # GC rate list
        self.dict = {} # fasta to dict, {key:name : value:seq}     
        self.df = '' # dataframe from fasta file
        # read file as lines
        with open(file_name)as file:
            lines = file.readlines()
            self.lines = lines
        # initial
        self.count_seq()
        self.lines2dict()
        self.add_features()
        self.lines2dataframe()

    ### initial functions ###

    def count_seq(self):# count seq num in a fasta file
        count = 0
        for line in self.lines:
            if line.startswith(">"):
                count += 1
        self.count = count
    
    def lines2dict(self) -> dict:
        dict = {}
        name = ''
        for line in self.lines:
            if line.startswith(">"):
                if name:
                    dict[name]= sequence
                line1 = line[1:]
                name = line1.split()[0]
                sequence = ''
            else:
                sequence += line
                
        dict[name]=sequence
        self.dict = dict

    def add_features(self):
        for name, content in self.dict.items():
            content = str(content).strip()
            simple_transcript_name = name.split()[0]
            self.gene_id.append(re.split('[-|.]', simple_transcript_name)[0])
            self.sequence.append(content)
            self.seq_len.append(len(content))
            self.transcript_name.append(name)

    def lines2dataframe(self) -> pd.DataFrame:
        '''
        e.g.
        ============================================================= 
        # |gene_id|transcript_name|sequence|seq_len|GC%|
        -- -------- --------------- ------- ------- --- -------------
        0  MH01g0010000 MH01t0010000-01 ATGCGTAGTCCTAAGTCCGATCGAT 277 40%
        1  MH01g0010000 MH01t0010000-02 ATGACTTTCAGCTGGGTACGTAT 255 33%
        =============================================================
        '''
        # self.add_features() # load features into dataframe
        df = pd.DataFrame({
                "gene_id":self.gene_id,
                "transcript_name":self.transcript_name,
                "sequence":self.sequence,
                "seq_len":self.seq_len
            })
        self.df = df

    ### pro functions ###

    def max_transcript(self, filename='out.fa') -> pd.DataFrame:
        '''
        @msg: out put max_transcript fasta file
        @param {*filename: out put path and filename}
        @return {*max_transcript dataframe}
        '''           
        df = self.df
        idx = df.groupby('gene_id')['seq_len'].idxmax()
        max_trans_df = df.iloc[idx].reset_index() # extract max trans according to idx
        with open(filename, 'w')as file:
            for i in max_trans_df.index:
                gene_id = max_trans_df['gene_id'][i]
                seq = max_trans_df['sequence'][i]
                file.write('>'+gene_id+'\n'+seq+'\n')
        return max_trans_df


    def extract_gene(self, gene_ids: list, filename='extract_result.fa', option = 'w', misls=False):
        dic = {}
        mismatch = []
        for gene_id in gene_ids:
            if gene_id in self.dict.keys():
                dic[gene_id] = self.dict[gene_id]
            else:
                mismatch.append(gene_id)
        if len(mismatch)==0:
            print('all matched')
        else:
            print(f'Match:{len(gene_ids)-len(mismatch)}; Mismatch:{len(mismatch)}')
            if misls:
                print(mismatch)
        dic2fa(dic, filename, option)


    def rename(self, rename_pattern, filename='out.fa'):
        ren_dict = {} # dictionary after rename
        with open(rename_pattern) as file:
            lines = file.readlines()
        for line in lines:
            old_name = line.split('\t')[0]
            new_name = line.split('\t')[1]
            ren_dict[new_name] = self.dict[old_name]
        dic2fa(ren_dict, filename)
        
######==========###### extern functions ######==========######
def dic2fa(dic, filename='out.fa', option ='w'):
    with open(filename, option)as file:
        for key, value in dic.items():
            file.write(">"+key+'\n'+ value.rstrip() +'\n')

if __name__ == '__main__':
    filename = 'E:\BaiduNetdiskWorkspace\PhDprogram\载体构建\genome\IRGSP-1.0_genome.fasta'
    Seq1 = Fasta(filename)
    # print(Seq1.lines)
    print(Seq1.dict['chr01'])
    # pd.set_option('display.max_columns', None) # display whole columns