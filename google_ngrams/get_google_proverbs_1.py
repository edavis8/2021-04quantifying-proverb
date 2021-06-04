from pathlib import Path
import os
import string
import argparse
import json
import re
import gzip

def make_args():
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
    files = []
    with open(infile, 'r') as myfile:
        for line in myfile:
            files += [line.rstrip()]
    return files

def gather_proverbs():
    proverbs= []
    with open('./all_proverbs.txt') as myfile:
        for row in myfile:
            proverbs+= [row]    
    proverbs = [a for a in proverbs if a != '\n']
    proverbs = [re.sub('.', '', a.strip()) for a in proverbs]
    proverbs_no_punc = [a.translate(str.maketrans('', '', string.punctuation)).lower() for a in proverbs]
    proverbs = set(proverbs)
    proverbs_no_punc = set(proverbs_no_punc)
    return proverbs, proverbs_no_punc

def read(myfile, filename, proverbs,proverbs_no_punc):
    full_text = myfile.read().decode('utf-8')
    instances = dict()

    instances['file'] = filename
    for proverb in proverbs:
        if len(re.findall(r"[\w']+|[.,!?;]", proverb))<=5:
            ex = ' '.join([gram+'(?:_w*)?' for gram in re.findall(r"[\w']+|[.,!?;]", proverb)])+'\t\d*\t\d*\t\d*'
            search = re.search(ex, full_text, flags = re.I)
            instances[proverb] = search
        
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
#    folder ='/users/c/d/cdanfort/scratch/google'
    files = get_filenames(infile)
    for filename in files:
        with gzip.open(filename) as myfile:
            a = read(myfile, filename, proverbs, proverbs_no_punc)
            proverbslist += [a]
    pdata = dict()
    pdata["data"] = proverbslist
    with open('./json_outs/'+outname , 'w') as fp:
        json.dump(pdata, fp)
    
    

