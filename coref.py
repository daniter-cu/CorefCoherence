import pickle
from collections import Counter, defaultdict

def parse_liwc():
    '''This is a subset of LIWC. It is used to identify pronouns'''
    with open("liwc_subset.pickle", "rb") as f:
        term_to_index_small = pickle.load(f)
    return term_to_index_small

def find_entry(word, term_to_index):
    '''Utility function to find index numbers by pronoun.
       Index numbers refer to LIWC classes.'''
    if word in term_to_index.keys():
        return term_to_index[word]
    else:
        for i in range(len(word), 0,-1):
            if word[:i]+"*" in term_to_index.keys():
                return term_to_index[word[:i]+"*"]
    return []

if __name__ == '__main__':
    # Load data that has already been convereted to coref chains
    with open("sample_data.pickle", "rb") as f:
        coref = pickle.load(f)

    term_to_index_small = parse_liwc()

    # This counter keeps number of ambiguous pronouns per speaker
    ambig_ref_counter = Counter()


    for speaker, text in coref.items():
        for refs in text:
            if len(refs[0].split()) == 1:
                entries = find_entry(refs[0], term_to_index_small)
                # If a 3rd person pronoun is seen as the first term in the ref
                # chain, it is considered an ambiguous pronoun
                # (4,5,6) are first, first plural and second person pronouns
                # so those must not be counted. 
                if 3 in entries and 4 not in entries and 5 not in entries and 6 not in entries:
                    ambig_ref_counter[speaker] += 1
    print (ambig_ref_counter)
