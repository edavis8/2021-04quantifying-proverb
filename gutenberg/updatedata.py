import json
from copy import deepcopy

f = open('./proverbs/alldata.txt', 'r')
data = json.load(f)
f.close()


g = open('/users/a/r/areagan/scratch/gutenberg/gutenberg-meta-append.json', 'r')
meta = []
for line in g:
    meta += [json.loads(line)]
g.close()

errors = []
update = deepcopy(data)
update2 = dict()
update2['all'] = []
for a in update['all']:
    update2['all'] += a

for book in update2['all']:
    obs = [a for a in meta if a['filename'] == book['file'][:-4]]
    try:
        obs = obs[0]
        title = obs['title']
        author = obs['author']
        language = obs['language']
        book['title'] = title
        book['author'] = author
        book['language'] = language
    except:
        error = book['file']
        errors += [error]
with open('./proverbs/alldata2.txt' , 'w') as myfile:
    json.dump(update, myfile)
with open('./proverbs/missing.txt', 'w') as myfile:
    for a in errors:
        myfile.write(a+'\n')

