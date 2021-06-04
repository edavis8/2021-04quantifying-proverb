import string
from pathlib import Path
import os
import argparse
import json
import re
from collections import Counter
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
    with open('all_proverbs.txt') as myfile:
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
    a2 = re.sub('[%s]' % re.escape(string.punctuation+'”“’'), ' ', a).lower()
    words = a2.split()
    one_grams = Counter(words)
    two_grams = Counter(zip(words, words[1:]))
    instances = dict()

    instances['file'] = filename
    for x in proverbs:
        locs = [(m.start(), m.end()) for m in re.finditer(x, a2)]
        if locs != []:
            instances[x] = [a2[max(0,l[0]-500):min(len(a2),l[1]+500)] for l in locs]
        
    return instances, one_grams, two_grams


if __name__ == '__main__':
    args = make_args()
    print('args made')
    infile = args.inputfile
    outname = str(infile).split('/')[1] + '.json'
    proverbs = gather_proverbs()
#    proverbs = ["silver lining", "every cloud has a silver lining", "every cloud has its silver lining","glass houses", "those who live in glass houses shouldn t throw stones","glass house",  "fool me once", "do unto others", "do onto others", "tilt at windmills", "tilting windmills", "tilt windmills", "tilting at windmills", "bird in the hand", "bird in hand", "count your chickens", "count ones chickens"]
    proverbslist = []
    ones = Counter()
    twos = Counter()
    folder ='/users/a/r/areagan/scratch/gutenberg/gutenberg-007/'
    files = get_filenames(infile)
    for filename in files:
        with open(folder+filename, 'r', encoding = 'utf-8') as myfile:
            a,one,two = read(myfile, filename)
            proverbslist += [a]
            ones += one
            twos += two
    pdata = proverbslist
    with open('neighborhoods/'+outname , 'w') as fp:
        json.dump(pdata, fp)
    with open('1grams/'+outname, 'w') as fp:
        json.dump(dict(ones), fp)
    with open('2grams/'+outname, 'w') as fp:
        json.dump({' '.join(i):twos[i] for i in twos}, fp)
    

    
