#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ethan Davis

Find proverbs in google books ngrams
Iterates through lines, matches regex pattern

Takes arguments: 
    -i --inputfile     job txt file with ngram corpus files to submit to server
    -g --gram          ngram length for proverb search 


"""

from pathlib import Path
import string
import argparse
import json
import re
import gzip



def make_args():
    """Set up arguments for command line"""
    description = 'get proverbs from google ngrams'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-i',
                        '--inputfile',
                        help='job file',
                        required=True,
                        type=valid_path)
    parser.add_argument('-g',
                        '--gram',
                        help='gram length',
                        required=True,
                        type=valid_path)

    return parser.parse_args()


def valid_path(p):
    return Path(p)

def get_filenames(infile):   
    """Retrive file names from job*.txt list"""
    
    files = []
    with open(infile, 'r') as myfile:
        for line in myfile:
            files += [line.rstrip()]
    return files



def gather_proverbs():
    """
    Retrieve proverbs from Mieder's Dictionary of American Proverbs (1992)
    Return with and without punctuation
    """
    proverbs= []
    with open('./Mieder-1992.txt') as myfile:
        for row in myfile:
            proverbs+= [row]    
    proverbs = [a for a in proverbs if a != '\n']
    proverbs = [re.sub('\.', '', a.strip()) for a in proverbs]
    proverbs_no_punc = [a.replace('--', ' ') for a in proverbs]
    proverbs_no_punc = [a.replace('-', ' ') for a in proverbs_no_punc]
    proverbs_no_punc = [a.translate(str.maketrans('', '', string.punctuation)) for a in proverbs_no_punc]
    proverbs = set(proverbs)
    proverbs_no_punc = set(proverbs_no_punc)
    proverbs_w_punc = proverbs - proverbs_no_punc
    return proverbs_w_punc, proverbs_no_punc



def read(myfile, filename, proverbs_w_punc,proverbs_no_punc, gramlen):  
    """
    Find proverbs in google ngram corpus file
    regex pattern match for each line
    returns instances in dict
    regex for proverbs with and without punctuation
    case insensitive 
    """
    instances = dict()
    instances['file'] = filename
    w_punc_gram = []
    
    #split proverbs into words and punctuation
    for proverb in proverbs_w_punc:
        resplit = re.findall(r"[^\W\']+|\'[\w']+|[\w']+|[.,!?;-]", proverb)
        if len(resplit)==gramlen:
            w_punc_gram.append(proverb)
    
    #split proverbs into words
    no_punc_gram = []
    for proverb in proverbs_no_punc:
        resplit = proverb.split()
        if len(resplit)==gramlen:
            no_punc_gram.append(proverb)
    
    #check each line for proverbs with and without punctuation
    for line in myfile:
        
        #with punctuation
        for proverb in w_punc_gram:
            resplit = re.findall(r"[^\W\']+|\'[\w']+|[\w']+|[.,!?;-]", proverb)
            if len(resplit)==gramlen and proverb[0].lower() == line[0].lower():
                ex = ' '.join([gram+'(?:_\w*)?' for gram in resplit])+'(?:\t\d*,\d*,\d*)*'
                search = re.findall(ex, line, flags = re.I)
                if search != [] and proverb in instances:
                    instances[proverb] += [line]
                elif search !=[]:
                    instances[proverb] = [line]
        
        #without punctuation        
        for proverb in no_punc_gram:
            if len(proverb.split())==gramlen and proverb[0].lower() == line[0].lower():
                ex = ' '.join([gram+'(?:_\w*)?' for gram in proverb.split()])+'(?:\t\d*,\d*,\d*)*'
                search = re.findall(ex, line, flags = re.I)     
                if search != [] and proverb in instances:
                    instances[proverb] += [line]
                elif search !=[]:
                    instances[proverb] = [line]

    return instances


if __name__ == '__main__':
    args = make_args()
    print('args made')
    infile = args.inputfile
    gramlen = int(str(args.gram))
    outname = str(infile) + '.json'
    proverbs, proverbs_no_punc = gather_proverbs()
    proverbslist = []
    files = get_filenames(infile)
    
    #read files and store results as .json
    for filename in files:
        with gzip.open(filename, 'rt') as myfile:
            result = read(myfile, filename, proverbs, proverbs_no_punc, gramlen)
            proverbslist += [result]
    with open('./json_outs/'+outname , 'w') as fp:
        json.dump(proverbslist, fp)

