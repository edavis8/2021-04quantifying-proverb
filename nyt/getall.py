#!/usr/bin/python
import os
import json
#from gutenberg.query import get_metadata

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

