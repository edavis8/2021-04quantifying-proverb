#!/usr/bin/bash

for F in $(cd jobtexts  && ls)
do
 sbatch neighborhoods.sh jobtexts/$F
 echo $F
done
