'''
Descripttion: 
version: 
Author: Roy White
Date: 2021-06-05 13:29:44
LastEditors: Please set LastEditors
LastEditTime: 2021-10-11 09:35:23
'''
import re
import dictdiffer
import pandas as pd
import statistic as stat
from collections import Counter
import itertools
import os
import OTFasta as otf
import sys
sys.path.append('E:\OmicsTools\omicstools')


def extract_gene(fa1: str, fa2: str, file: str):
    # extract gene, from another fasta or a gene name list
    Fa2 = otf.Fasta(fa2)
    if (type(fa1).__name__ == 'str'):  # fa1 is a filename
        Fa1 = otf.Fasta(fa1)
        Fa2.extract_gene(Fa1.gene_id, file)
    elif (type(fa1).__name__ == 'list'):  # fa1 is a name list
        Fa2.extract_gene(fa1, file)


if False:
    def merge_fasta(fa1: str, fa2: str, file: str):
        # merge 2 fasta file, delete the same gene
        Fa1 = otf.Fasta(fa1)
        Fa2 = otf.Fasta(fa2)
        # d = dict(Fa1.dict, **Fa2.dict) # result dict # python < 3.9
        d = Fa1.dict | Fa2.dict  # python 3.9
        otf.dic2fa(d, file)


def merge_fasta(falist: list, file: str):
    Falist = [otf.Fasta(fa).dict for fa in falist]
    for i in range(len(Falist)-1):
        Falist[i+1] |= Falist[i]  # python3.9
    d = Falist[i+1]
    otf.dic2fa(d, file)


def easy_blast(db: str, db_type: str, query: str, query_type: str, out: str, evalue='10', outfmt='6'):
    '''
    @param {str} db
    @param {str} db_type: nucl or prot
    @param {str} query
    @param {str} query_type: nucl or prot
    @param {str} out
    @param {str} evalue: default '10'
    @param {str} outfmt: default '6'
    @return {None}
    '''
    # build blast database
    query_simplify = query.removesuffix(
        '.fas').removesuffix('.fa').removesuffix('.fasta').removesuffix('.txt')
    db_simplify = db.removesuffix('.fa').removesuffix(
        '.fas').removesuffix('.fasta').removesuffix('.txt')
    db_name = db_simplify + '.db'  # database name, consis of infile + db
    flag = os.system(f'makeblastdb -in {db} -out {db_name} -dbtype {db_type} -parse_seqids')
    if flag:
        print("something wrong, database doesn't build correctly")
        sys.exit(0)  # kill program
    '''
    blastn -db database_name -query input_file -out output_file -evalue evalue -max_target_seqs num_sequences -num_threads int_value -outfmt format format_string
    blastn -db database_name -query input_file -out output_file -evalue evalue -max_target_seqs num_sequences -num_threads int_value -outfmt format "7 qacc sacc evalue length pident"
    '''
    # blast program
    # choose program
    dict = {
        ('prot', 'prot'): 'blastp',
        ('prot', 'nucl'): 'tblastn',
        ('nucl', 'prot'): 'blastx',
        ('nucl', 'nucl'): 'blastn'
    }
    if not out:
        out = query_simplify + '2' + db_simplify.split('\\')[-1] + '.blastout'
    # Command line argument error:
    # Argument "out". File is not accessible:
    # `D:\Document\PhDprogram\WAKgenefamily\MH\MH63WAK2D:\Document\PhDprogram\WAKgenefamily\ZS\ZS97WAK'
    # blastn, blastp, tblastn, tblastx
    blast_program = dict[query_type, db_type]
    # run, return 0, else return 1;
    flag = os.system(
        f'{blast_program} -query {query} -db {db_name} -out {out} -evalue {evalue} -outfmt {outfmt}')
    if flag:
        print("something wrong, blast doesn't run correctly")
        sys.exit(0)


def create_kmers(k):  # creat all possible kmers which lenth is k
    bases = ['A', 'T', 'C', 'G']
    kmers = [''.join(i) for i in itertools.product(bases, repeat=k)]

    return kmers


def gene_to_kmers(seq, k):  # split gene into kmers
    kmers = []
    seq = seq.upper()
    for start in range(0, len(seq)-(k-1), 1):
        kmer = seq[start:start+k]
        kmers.append(kmer)

    return kmers


def counter_kmers(kmers: list, n: int) -> dict:  # counter kmers and find most common
    # be careful! this program is too slow!
    kmers_fre = Counter(kmers).most_common(n)

    return dict(kmers_fre)


def venn(list1, list2) -> list:
    list_both = list(set(list1) & set(list2))
    list_1 = list(set(list1).difference(list2))
    list_2 = list(set(list2).difference(list1))

    return list_both, list_1, list_2


def readTXT(filename):
    with open(filename)as f:

        return f.readlines()


def readExcel(filename, sheet_name):
    data = pd.read_excel(filename, sheet_name)

    return(data)  # pd.Dataframe


def get_FileSize(filePath):
    fsize = os.path.getsize(filePath)
    fsize = fsize/float(1024 * 1024)

    return round(fsize, 2)


def compare_fasta(fa1, fa2):
    Fa1 = otf.Fasta(fa1)
    Fa2 = otf.Fasta(fa2)
    differ = dictdiffer.diff(Fa1.dict, Fa2.dict)
    # df = pd.DataFrame(differ)
    # print(df)

    change = []  # the same key, different value
    add = []  # in 2 but not 1
    remove = []  # in 1 but not 2
    for item in differ:
        if item[1]:
            change.append(item[1])
        if item[0] == 'add':
            a, b = zip(*item[2])
            add = list(a)
        if item[0] == 'remove':
            a, b = zip(*item[2])
            remove = list(a)

    same = []
    for key in list(Fa1.dict.keys() & Fa2.dict.keys()):
        if Fa1.dict[key] == Fa2.dict[key]:
            same.append(key)

    return change, add, remove, same


def reverse_complement(sequence):
    # trantab = str.maketrans(intab, outtab)   # 制作翻译表
    trantab = str.maketrans('ACGTacgtRYMKrymkVBHDvbhd',
                            'TGCAtgcaYRKMyrkmBVDHbvdh')
    string = sequence.translate(trantab)     # str.translate(trantab)  # 转换字符
    return string[::-1]


def crispr_primer_designer(sgRNA):
    # Only for pTCK303
    while True:
        if len(sgRNA) == 20:
            forward = 'TAGGTCTCC' + sgRNA[8:] + 'GTTTTAGAGCTAGAA'
            reward = 'CGGGTCTCA' + \
                reverse_complement(sgRNA[:12]) + 'TGCACCAGCCGGG'
            return f'F:{forward}\nR:{reward}\n'

        elif len(sgRNA) == 23:
            sgRNA = sgRNA[:20]
            continue

        else:
            return False


    # forwardp = 'ACGACGGCCAGTGCCAAGCTT'
    # rewardp = 'TATGACCATGATTACGAATTC'
def infusion_primer_designer(targetDNA, forwardp, rewardp):
    '''
    parameters: 
        targetDNA:目的基因，用于提取其基因特异性同源序列
        forwardp: 质粒同源序列F 正链5'-3'
        rewardp: 质粒同源序列R 正链5'-3'
        cuttingsite: 酶切位点
    '''
    # for 
    forwardDNA = targetDNA[:19] # 从目标基因上选取前20bp 正链 5'-3'
    rewardDNA = targetDNA[-19:] # 从目标基因上选取后20bp 正链 5'-3'
    forward = forwardp + forwardDNA # 正链 5'-3'
    reward = reverse_complement(rewardDNA + rewardp) # 负链 5'-3'
    cutsit_dic = {
                "ApaI":" GGGCCC",
                "BamHI":" GGATCC",
                "BglII":" AGATCT",
                "EcoRI":" GAATTC",
                "HindIII":"AAGCTT",
                "KpnI":" GGTACC",
                "NcoI":" CCATGG",
                "NdeI":" CATATG",
                "NheI":" GCTAGC",
                "NotI":" GCGGCCGC",
                "SacI":" GAGCTC",
                "SalI":" GTCGAC",
                "SphI":" GCATGC",
                "XbaI":" TCTAGA",
                "XhoI":" CTCGAG"}
                
    return f'F:{forward}\nR:{reward}\n'
    

def get_directory(string):
    pattern = re.compile(r'\\[^\\]+$')
    # string = r'E:\BaiduNetdiskWorkspace\omicstools\tests.txt'
    return re.sub(pattern, '', string)


if __name__ == '__main__':
    forwardp = "CAGGTCGACTCTAGAGGATCC" # BamHI
    rewardp = 'GGTACCATGGGAAGATCTACT' # KpnI
    with open(r'E:\BaiduNetdiskWorkspace\PhDprogram\Mechano-sensitive_protein\01_Method\CRISPR_overexpression_GFP\gene_candidates\基因信息\MCA1.fa') as f:
        lines = f.readlines()
        targetDNA =''
        for line in lines[1:]:
            targetDNA += line
    targetDNA = targetDNA.strip()

    print(infusion_primer_designer(targetDNA, forwardp, rewardp))
    print(reverse_complement('GGTACCATGGGAAGATCTACT'))