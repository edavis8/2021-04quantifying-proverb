#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 17 11:37:52 2020

@author: admin
"""
from xml.etree import ElementTree as et
import re
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
    with open('./all_proverbs.txt') as myfile:
        for row in myfile:
            l+= [row]    
    l2 = [a for a in l if a != '\n']
    l3 = [a.strip('\n') for a in l2]
    l4 = [a.translate(str.maketrans('', '', string.punctuation)).lower() for a in l3]
    proverbs = set(l4)
    proverbs.remove('s')
    return proverbs

def read(myfile, filename):
    tree = et.parse(filename)
    root = tree.getroot()
    
    body = tree.getiterator('body.content')[0]
    head = tree.find('head')
    
    title = head.findall('title')[0].text if head.findall('title') != [] else None
    author = tree.getiterator('byline')[0].text if tree.getiterator('byline') != [] else None
    meta = head.findall('meta')
    section = [a.get('content') for a in meta if a.get('name') == 'online_sections']
    day = [a.get('content') for a in meta if a.get('name') == 'publication_day_of_month']
    day_week = [a.get('content') for a in meta if a.get('name') == 'publication_day_of_week']
    month = [a.get('content') for a in meta if a.get('name') == 'publication_month']
    year = [a.get('content') for a in meta if a.get('name') == 'publication_year']
    full_text = [a for a in body if a.get('class') == 'full_text']
    full_text = full_text[0] if full_text !=[] else []
    metadata = {'title':title, 'author':author, 'section':section, 'day':day, 'day_week': day_week, 'month':month, 'year':year}
    ps = [a.text for a in full_text]
    text = ' '.join(ps)
    text_clean = re.sub('[%s]' % re.escape(string.punctuation+'”“’'), ' ', text).lower()
    instances = dict()
    instances['metadata'] = metadata
    for x in proverbs:
        if x in text_clean:
            instances[x] = text_clean.count(x)
            
    if all([a==[] or a == metadata for a in instances.values()]) == True:
        return None
    else:
        return instances
    

if __name__ == '__main__':
    args = make_args()
    print('args made')
    infile = args.inputfile
    outname = str(infile)[24:-4]+'.json'
    proverbs = gather_proverbs()
    proverbslist = []
    files = get_filenames(infile)
    for filename in files:
        try:
            with open(filename, 'r', encoding = 'utf-8') as myfile:
                a = read(myfile, filename)
                if a != None:
                    proverbslist += [a]
        except:
            continue
    pdata = dict()
    pdata["data"] = proverbslist
    with open('./nyt_outs_non_tar/'+outname , 'w') as fp:
        json.dump(pdata, fp)
    

