import string
from pathlib import Path
import os
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
    a2 = re.sub('[%s]' % re.escape(string.punctuation+'”“’'), ' ', a).lower()
    instances = dict()

    instances['file'] = filename
    for x in proverbs:
        matches = [m for m in re.finditer(x, a2)]
        instances[x] = [{m.group():a[max(0,m.span()[0]-1000):min(len(a),m.span()[1]+1000)]} for m in matches]
    if all([a==[] or a == filename for a in instances.values()]) == True:
        return None
    else:
        return instances


if __name__ == '__main__':
    args = make_args()
    print('args made')
    infile = args.inputfile
    outname = str(infile)[18:-4] + '.json'
#    proverbs = gather_proverbs()
    proverbs = ['the only good (?P<name>\w+) is a dead (?P=name)', 'the only good indian is a dead indian','big (?P<name>\w+) eat little (?P=name)','big fish eat little fish', \
                'a picture is worth a thousand words', 'a picture is worth (.{,50}?) words', \
                'an apple a day keeps the doctor away', '(a|an) (\w+) a day keeps the (\w+) away', \
                '(\w+) throw the baby out with the bath water', '(don t|dont|do not) throw the baby out with the bath water', 'baby (.{,100}?) bath water',\
                'call a spade a spade', 'call (a|an) (?P<name>\w+) (a|an) (?P=name)', '(don t|\w+) swap horses in the middle of the stream',\
                'good fences make good neighbors', 'good (\w+) make good (\w+)', 'a house divided against itself cannot stand',\
                'right makes might']
    proverbslist = []
    folder ='/users/a/r/areagan/scratch/gutenberg/gutenberg-007/'
    files = get_filenames(infile)
    for filename in files:
        with open(folder+filename, 'r', encoding = 'utf-8') as myfile:
            a = read(myfile, filename)
        if a == None:
            continue
        proverbslist += [a]
    pdata = dict()
    pdata["data"] = proverbslist
    with open('./proverbs/specific_outs2/'+outname , 'w') as fp:
        json.dump(pdata, fp)
    

