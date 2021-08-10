"""

Ethan Davis

Get proverbs from gutenberg
Get neighboring 1gram and 2grams
Investigate language surrounding proverbs
For later use with Allotaxonometer

Takes arguments: 
    -i --inputfile     job*.txt file with nyt corpus files to submit to server

"""



import string
from pathlib import Path
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
    proverbs = []
    with open('all_proverbs.txt') as myfile:
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
    text = re.sub('[%s]' % re.escape(string.punctuation+'”“’'), ' ', text).lower()
    words = text.split()
    one_grams = Counter(words)
    two_grams = Counter(zip(words, words[1:]))
    instances = dict()

    instances['file'] = filename
    for proverb in proverbs:
        locs = [(m.start(), m.end()) for m in re.finditer(proverb, text)]
        if locs != []:
            instances[proverb] = [text[max(0,l[0]-500):min(len(text),l[1]+500)] for l in locs]
        
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
    

    
