"""

Ethan Davis

Get proverbs from Gutenberg documents

Takes arguments: 
    -i --inputfile     job*.txt file with nyt corpus files to submit to server

"""


import string
from pathlib import Path
import argparse
import json



def make_args():
    description = 'get proverbs from gutenberg books'
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
    proverbs = []
    with open('./proverbs/all_proverbs.txt') as myfile:
        for row in myfile:
            proverbs+= [row]    
    proverbs = [a for a in proverbs if a != '\n']
    proverbs = [a.strip('\n') for a in proverbs]
    proverbs = [a.translate(str.maketrans('', '', string.punctuation)).lower() for a in proverbs]
    proverbs = set(proverbs)
    return proverbs

def read(myfile, filename):
    doc = []
    for row in myfile:
        doc += [row.rstrip()]
    text = ' '.join(doc)
    
    #remove punctuation from file
    text = text.translate(str.maketrans('', '', string.punctuation+'”“’')).lower()
    
    instances = dict()

    instances['file'] = filename
    for proverb in proverbs:
        if proverb in text:
            instances[proverb] = text.count(proverb)

    return instances


if __name__ == '__main__':
    args = make_args()
    print('args made')
    infile = args.inputfile
    outname = str(infile)[18:-4] + '.json'
    proverbs = gather_proverbs()
    proverbslist = []
    folder ='/users/a/r/areagan/scratch/gutenberg/gutenberg-007/'
    files = get_filenames(infile)
    for filename in files:
        with open(folder+filename, 'r', encoding = 'utf-8') as myfile:
            a = read(myfile, filename)
            proverbslist += [a]
    pdata = dict()
    pdata["data"] = proverbslist
    with open('./proverbs/json_outs/'+outname , 'w') as fp:
        json.dump(pdata, fp)
    
    
