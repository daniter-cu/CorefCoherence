import os
import numpy as np
import pickle
from collections import Counter, defaultdict

def parse_liwc():
    with open("liwc_subset.pickle", "rb") as f:
        term_to_index_small = pickle.load(f)
    return term_to_index_small

def find_entry(word, term_to_index):
    if word in term_to_index.keys():
        return term_to_index[word]
    else:
        for i in range(len(word), 0,-1):
            if word[:i]+"*" in term_to_index.keys():
                return term_to_index[word[:i]+"*"]
    return []

if __name__ == '__main__':
    with open("../data/coref/corefs_plus_new_data.pickle", "rb") as f:
        coref = pickle.load(f)

    term_to_index_small = parse_liwc()
    c = Counter()
    for k, interview in coref.items():
        for i, response in enumerate(interview):
            for j, refs in enumerate(response):
                if len(refs[0].split()) == 1:
                    entries = find_entry(refs[0], term_to_index_small)
                    if 3 in entries and 4 not in entries and 5 not in entries and 6 not in entries:
                        c[k] += 1
    print (c)
