from pathlib import Path
import string
import argparse
import json
import re
import gzip
def make_args():
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
    proverbs = [re.sub('\.', '', a.strip()) for a in proverbs]
    proverbs_no_punc = [a.replace('--', ' ') for a in proverbs]
    proverbs_no_punc = [a.replace('-', ' ') for a in proverbs_no_punc]
    proverbs_no_punc = [a.translate(str.maketrans('', '', string.punctuation)) for a in proverbs_no_punc]
    proverbs = set(proverbs)
    proverbs_no_punc = set(proverbs_no_punc)
    proverbs_w_punc = proverbs - proverbs_no_punc
    return proverbs_w_punc, proverbs_no_punc

def read(myfile, filename, proverbs_w_punc,proverbs_no_punc, gramlen):  
    all_file = myfile.read()
    instances = dict()
    instances['file'] = filename
#    while line != '':
    for proverb in proverbs_w_punc:
        resplit = re.findall(r"[^\W\']+|\'[\w']+|[\w']+|[.,!?;-]", proverb)
        if len(resplit)==gramlen:
            print(resplit)
            ex = ' '.join([gram+'(?:_\w*)?' for gram in resplit])+'(?:\t\d*,\d*,\d*)*'
            search = re.findall(ex, all_file, flags = re.I)
            if search != []:
                print(search)
                instances[proverb] = search
    
            
    for proverb in proverbs_no_punc:
        if len(proverb.split())==gramlen:
            print(proverb)
            ex = ' '.join([gram+'(?:_\w*)?' for gram in proverb.split()])+'(?:\t\d*,\d*,\d*)*'
            search = re.findall(ex, all_file, flags = re.I)     
            if search != []:
                print(search)
                instances[proverb] = search
     #   line = myfile.readline().decode('utf-8')
    return instances


if __name__ == '__main__':
    args = make_args()
    print('args made')
    infile = args.inputfile
    gramlen = int(str(args.gram))
    outname = str(infile) + '.json'
    proverbs, proverbs_no_punc = gather_proverbs()
    proverbslist = []
#    folder ='/users/c/d/cdanfort/scratch/google'
    files = get_filenames(infile)
    for filename in files:
        with gzip.open(filename, 'rt') as myfile:
            a = read(myfile, filename, proverbs, proverbs_no_punc, gramlen)
            proverbslist += [a]
    #pdata = dict()
    #pdata["data"] = proverbslist
    with open('./json_outs/'+outname , 'w') as fp:
        json.dump(proverbslist, fp)
    
 
