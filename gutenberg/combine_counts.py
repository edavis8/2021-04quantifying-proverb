import os
import json
from collections import Counter
counts = Counter()
for fname in os.listdir('1grams'):
    with open('1grams/'+fname, 'r') as file:
        d = json.load(file)
        counts += Counter(d)

with open('gutenberg_1grams.json', 'w') as file:
    json.dump(dict(counts),file )
