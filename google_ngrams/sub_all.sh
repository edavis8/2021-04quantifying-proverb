#!/usr/bin/bash

for F in $(cd 3gram_jobs  && ls)
do
 sbatch google_proverbs.sh 3gram_jobs/$F 3
 echo $F
done
