#!/bin/bash
#SBATCH -p bluemoon
#SBATCH -N 1
#SBATCH --mem-per-cpu=8G
#SBATCH --time=4:00:00
#SBATCH --job-name=ngram_gut
#SBATCH --mail-user=ethan.davis@uvm.edu
cd $HOME/proverbs/gutenberg
echo "running on " `hostname`
python combine_counts.py
