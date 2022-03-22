#!/bin/bash

#use the current working directory and current modules
#$ -cwd -V

#$ -b y -l mem_free=16G -P jravel-lab -q threaded.q -pe thread 4 -N consortia_mapping -j y -o /local/scratch/mfrance/logs/ -e /local/scratch/mfrance/logs/

#setting the number of jobs to be executed
#$ -t 1-3

cd /local/scratch/mfrance/PGATES/VCHIP/03_mapping/

seq_dir=/local/scratch/mfrance/PGATES/VCHIP/01_preprocess/1_fastq_pe

infile=`sed -n -e "$SGE_TASK_ID p" redo.lst`


sample=$(echo $infile | cut -f1 -d,)
reference=$(echo $infile | cut -f2 -d,)

bowtie2 --local --no-unal -L 18 -N 1 -p 4 -x ./reference/$reference/$reference -1 $seq_dir/${sample}.R1.fq.gz -2 $seq_dir/${sample}.R2.fq.gz -U $seq_dir/${sample}.unpaired.fq.gz -S ${sample}_pred.sam

samtools view -bT ./reference/$reference/${reference}_marker_genes.fa ${sample}_pred.sam > ${sample}_pred.bam

rm ${sample}_pred.sam

samtools sort -o ${sample}_pred_s.bam -T ${sample}-TEMP ${sample}_pred.bam 

rm ${sample}_pred.bam

samtools depth -a ${sample}_pred_s.bam > ${sample}.depth

rm ${sample}_pred_s.bam

python contig_cov_calc.py ${sample}
