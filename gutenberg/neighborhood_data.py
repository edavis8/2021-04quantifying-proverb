import os
import json
from collections import Counter
one_grams = Counter()
two_grams = Counter()
for fname in os.listdir('neighborhoods'):
    with open('neighborhoods/'+fname,'r') as myfile:
        data = json.load(myfile)
        for prov in data:
            for l in data[prov]:
                l = l.replace(prov, '')
                words = l.split()
                mid = int(len(words/2))
                words = words[max(mid-20, 0):min(mid+20,len(words)]
                ones = Counter(words)
                twos = Counter(zip(words, words[1:]))
                one_grams += ones
                two_grams += twos

with open('1gram_neighborhoods.json', 'w') as myfile:
    json.dump(dict(one_grams), myfile)

with open('2gram_neighborhoods.json', 'w') as myfile:
    json.dump({' '.join(i):twos[i] for i in twos}, fp)
