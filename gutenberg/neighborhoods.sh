#!/bin/bash
#SBATCH -p bluemoon
#SBATCH -N 1
#SBATCH --mem-per-cpu=4G
#SBATCH --time=8:00:00
#SBATCH --job-name=ngram_proverbs
#SBATCH --mail-user=ethan.davis@uvm.edu
cd $HOME/proverbs/gutenberg
echo "running on " `hostname`
file=$1
python get_neighborhood.py -ifile ${file}
