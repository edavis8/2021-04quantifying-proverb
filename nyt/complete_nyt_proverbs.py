#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""

Ethan Davis

Get proverbs from the nyt annotated corpus
Reads xml files and finds proverbs in article text
Get metadata from articles with proverbs

Takes arguments: 
    -i --inputfile     job*.txt file with nyt corpus files to submit to server

"""
from xml.etree import ElementTree as et
import re
import string
from pathlib import Path
import os
import argparse
import json
import subprocess
import tarfile

def make_args():
    description = 'get proverbs from nyt corpus'
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

def gather_proverbs():
    """
    Retrieve proverbs from Mieder's Dictionary of American Proverbs (1992)
    Return with and without punctuation
    """
    
    proverbs= []
    with open('./all_proverbs.txt') as myfile:
        for row in myfile:
            proverbs+= [row]    
    proverbs = [a for a in proverbs if a != '\n']
    proverbs = [a.strip('\n') for a in proverbs]
    proverbs = [a.translate(str.maketrans('', '', string.punctuation)).lower() for a in proverbs]
    proverbs = set(proverbs)
    return proverbs

def read(myfile, filename):
    """
    Get proverbs from articles from nyt corpus files
    reads xml data, returns dict with proverbs and metadata
    case insensitive 
    """
    
    tree = et.parse(myfile)
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
    outname = str(infile)[16:-4]+'_comp.json'
    proverbs = gather_proverbs()
    proverbslist = []
    tarfiles = get_filenames(infile)
    file_loc = '/users/p/d/pdodds/data/2010-01nytimes/data/'
    #read through tar files and output json with proverbs
    for tar_loc in tarfiles:
        tar_open = tarfile.open(tar_loc)
        xmls = subprocess.Popen(['tar', '-tf', tar_loc, '*.xml'], stdout = subprocess.PIPE)
        lines = xmls.stdout.readlines()
        tar_xmls = [a.decode().rstrip() for a in lines]
        for xml_file in tar_xmls:
            with tar_open.extractfile(xml_file) as myfile:
                a = read(myfile, xml_file)
                if a!= None:
                    proverbslist += [a]   
    pdata = dict()
    pdata["data"] = proverbslist
    with open('./nyt_outs/'+outname , 'w') as fp:
        json.dump(pdata, fp)
    

