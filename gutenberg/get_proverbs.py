import string
from pathlib import Path
import os
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
    l= []
    with open('./proverbs/all_proverbs.txt') as myfile:
        for row in myfile:
            l+= [row]    
    l2 = [a for a in l if a != '\n']
    l3 = [a.strip('\n') for a in l2]
    l4 = [a.translate(str.maketrans('', '', string.punctuation)).lower() for a in l3]
    proverbs = set(l4)
    proverbs.remove('s')
    return proverbs

def read(myfile, filename):
    d = []
    for row in myfile:
        d += [row.rstrip()]
    a = ' '.join(d)
    a2 = a.translate(str.maketrans('', '', string.punctuation+'”“’')).lower()
    
    instances = dict()

    instances['file'] = filename
    for x in proverbs:
        if x in a2:
            instances[x] = a2.count(x)

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
    
    
