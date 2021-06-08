#!/usr/bin/python
"""
Ethan Davis

combining json outputs from google books proverbs
"""
import os
import json

def combine():
    proverb_data = []
    path = './json_outs/'
    for a in os.listdir(path):
        with open(path+a, 'r') as myfile:
            j = json.load(myfile)
        proverb_data+=j
    with open('google_proverbs.json', 'w') as fp:
        json.dump(proverb_data, fp)
        
if __name__ == '__main__':
    combine()
    
