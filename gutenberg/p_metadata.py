import json
import pickle
objects = []
with (open("/users/a/r/areagan/scratch/gutenberg/all-book-metadata-raw-51249.p", "rb")) as openfile:
    while True:
        try:
            objects.append(pickle.load(openfile))
        except EOFError:
            break

d = dict()
d['data'] = objects
with open('metadata.json', 'w') as myfile:
    json.dump(d, myfile)

