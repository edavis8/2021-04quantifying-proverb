#!/usr/bin/python

"""
Ethan Davis

find proverbs in google books ngrams
using regex search (re.search())

For now, ended up being slower than get_google_proverbs_iter.py

Still, may be useful for future pattern matching


Takes arguments: 
    -i --inputfile     job txt file with ngram corpus files to submit to server
    -g --gram          ngram length for proverb search 



"""


from pathlib import Path
import os
import string
import argparse
import json
import re
import gzip

def make_args():
    """Set up arguments for command line"""
    description = 'get proverbs from google ngrams'
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument('-ifile',
                        '--inputfile',
                        help='path to input directory of books',
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
    proverbs = [re.sub('.', '', a.strip()) for a in proverbs]
    proverbs_no_punc = [a.translate(str.maketrans('', '', string.punctuation)).lower() for a in proverbs]
    proverbs = set(proverbs)
    proverbs_no_punc = set(proverbs_no_punc)
    return proverbs, proverbs_no_punc

def read(myfile, filename, proverbs,proverbs_no_punc):
    """
    Find proverbs in google ngram corpus file
    regex pattern match for each line
    returns instances in dict
    regex for proverbs with and without punctuation
    case insensitive 
    """
    
    full_text = myfile.read().decode('utf-8')
    instances = dict()

    instances['file'] = filename
    
    #split proverbs into words and punctuation
    #and search in google ngram file
    for proverb in proverbs:
        if len(re.findall(r"[\w']+|[.,!?;]", proverb))<=5:
            ex = ' '.join([gram+'(?:_w*)?' for gram in re.findall(r"[\w']+|[.,!?;]", proverb)])+'\t\d*\t\d*\t\d*'
            search = re.search(ex, full_text, flags = re.I)
            instances[proverb] = search
    
    
    #split proverbs into words   
    #and search in google ngram file
    for proverb in proverbs_no_punc:
        if len(proverb.split())<=5:
            ex = ' '.join([gram+'(?:_w*)?' for gram in proverb.split()])+'\t\d*\t\d*\t\d*'
            search = re.search(ex, full_text, flags = re.I)     
            instances[proverb] = search
    
    return instances


if __name__ == '__main__':
    args = make_args()
    print('args made')
    infile = args.inputfile
    outname = str(infile)[18:-4] + '.json'
    proverbs, proverbs_no_punc = gather_proverbs()
    proverbslist = []
    files = get_filenames(infile)
    
    #read files and store results as .json
    for filename in files:
        with gzip.open(filename) as myfile:
            a = read(myfile, filename, proverbs, proverbs_no_punc)
            proverbslist += [a]
    pdata = dict()
    pdata["data"] = proverbslist
    with open('./json_outs/'+outname , 'w') as fp:
        json.dump(pdata, fp)
    
    

