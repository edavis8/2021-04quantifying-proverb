
#!/usr/bin/env python3
"""
Ethan Davis

Investigate varied phrasing of proverbs in gutenberg
ex. "every cloud has a/its silver lining" or just "silver lining"

Takes arguments: 
    -i --inputfile     job*.txt file with nyt corpus files to submit to server

"""


import string
from pathlib import Path
import argparse
import json
import re

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
    """get file names from job*.txt file"""
    files = []
    with open(infile, 'r') as myfile:
        for line in myfile:
            files += [line.rstrip()]
    return files



def read(myfile, filename):
    """
    Find instances of varied phrasing and proverbial expressions for several proverbs
    also returns the context (surrounding words) of use
    case insensitive and no punctuation
    """
    words = []
    for row in myfile:
        words += [row.rstrip()]
    words_w_punc = ' '.join(words)
    words = re.sub('[%s]' % re.escape(string.punctuation+'”“’'), ' ', words_w_punc).lower()
    instances = dict()

    instances['file'] = filename
    for x in proverbs:
        locs = [m.start() for m in re.finditer(x, words)]
        instances[x] = [words[max(0,l-1000):min(len(words),l+1000)] for l in locs]
        
    return instances


if __name__ == '__main__':
    args = make_args()
    print('args made')
    infile = args.inputfile
    outname = str(infile)[18:-4] + '.json'
    proverbs = ["silver lining", "every cloud has a silver lining", "every cloud has its silver lining","glass houses", "those who live in glass houses shouldn t throw stones","glass house",  "fool me once", "do unto others", "do onto others", "tilt at windmills", "tilting windmills", "tilt windmills", "tilting at windmills", "bird in the hand", "bird in hand", "count your chickens", "count ones chickens"]
    proverbslist = []
    folder ='/users/a/r/areagan/scratch/gutenberg/gutenberg-007/'
    files = get_filenames(infile)
    for filename in files:
        with open(folder+filename, 'r', encoding = 'utf-8') as myfile:
            a = read(myfile, filename)
            proverbslist += [a]
    pdata = dict()
    pdata["data"] = proverbslist
    with open('./proverbs/specific_outs/'+outname , 'w') as fp:
        json.dump(pdata, fp)
    
    
