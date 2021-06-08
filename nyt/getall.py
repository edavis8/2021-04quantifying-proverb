#!/usr/bin/python

"""""
Ethan Davis
collect json files into single file nyt corpus
"""
import os
import json

def collect():
    proverb_data = dict()
    proverb_data['all'] = []
    path = './nyt_outs/'
    for a in os.listdir(path):
        with open(path+a, 'r') as myfile:
            for line in myfile:
                f = json.loads(line)
                proverb_data['all'] += f['data']
    with open('nyt_new.json', 'w') as fp:
        json.dump(proverb_data, fp)
        
    
if __name__ == '__main__':
    collect()

