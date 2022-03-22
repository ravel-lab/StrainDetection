#!/usr/bin/python3
import sys
import pandas as pd
from Bio.SeqIO.FastaIO import SimpleFastaParser
import re
from Bio.Align.Applications import MuscleCommandline

with open(sys.argv[2]) as fasta_file:
    headers = []
    seqs = []
    for rec, sequence in SimpleFastaParser(fasta_file):
        headers.append(rec)
        seqs.append(str(sequence))

fasta_df = pd.DataFrame(dict(header=headers, seq=seqs)).set_index(['header'])
fasta_df['Genome'] = fasta_df.index.str.split("|").str[0]
fasta_df['Length'] = fasta_df['seq'].str.len()


strain_bank = ['C0059E1','C0112A1','C0006A1','C0020A1','C0028A1','C0022A1','C0175A1','C0124A1']
not_needed = ['C0124A1','C0028A1','C0006A1','C0022A1','C0112A1']

orthologFastaOut = open('%s_marker_genes.fa' %(sys.argv[3]),'w')

with open(sys.argv[1]) as orthologs: 

    for cnt, ortholog in enumerate(orthologs):

        (orthoID,geneList) = ortholog.split(":")
        geneList = geneList.rstrip().split(" ")[1:]

        for strain in not_needed:
            geneList=[x for x in geneList if strain not in x]

        if len(geneList) == 1:

            print(geneList)

            orthologSeqsDF = fasta_df.loc[geneList].sort_values(['Genome','Length'],axis=0,ascending=False).reset_index()
            orthologSeqsDF = orthologSeqsDF.groupby("Genome").first().reset_index()

            for index,row in orthologSeqsDF.iterrows():

                orthologFastaOut.write('>'+row['header']+'\n'+row['seq']+'\n')

orthologFastaOut.close()