#!/bin/bash
#SBATCH -p bluemoon
#SBATCH -N 1
#SBATCH --mem-per-cpu=8G
#SBATCH --time=16:00:00
#SBATCH --job-name=ngram_proverbs
#SBATCH --mail-user=ethan.davis@uvm.edu
cd $HOME/proverbs/google_ngrams
echo "running on " `hostname`
file=$1
gram=$2
python get_iter_1.py -i ${file} -g ${gram}

