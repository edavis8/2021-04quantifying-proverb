#!/usr/bin/python
import os
import json
#from gutenberg.query import get_metadata

#proverb_data = dict()
proverb_data = []
path = './json_outs/'
for a in os.listdir(path):
    with open(path+a, 'r') as myfile:
        j = json.load(myfile)
    proverb_data+=j
with open('google_proverbs.json', 'w') as fp:
    json.dump(proverb_data, fp)

