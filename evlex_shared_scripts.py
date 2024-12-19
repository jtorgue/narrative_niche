from collections import defaultdict, Counter
import csv

good_pos = {'NOUN','ADJ','VERB'}
excluded_lemmas = {'be', 'other', 'have', 'let', 'one', 'lot', 'same', 'such', 't', 's'}

def select_genres(corpus, files_metadata, genres):
    metadata = csv.DictReader(open(files_metadata), delimiter='\t')
    metadata = {(x['doculect'][:4],x['file']): (x['genre'],int(x['tokens'])) for x in metadata}
    genre_counts = Counter()
    new_corpus = defaultdict(lambda : {})
    for f in corpus:
        for fi in corpus[f]:
            fx = '_'.join(fi.split('_')[2:])
            genre = metadata[f[:4],fx][0]
            genre_counts[genre] += 1
            if genre in genres:
                new_corpus[f][fi] = corpus[f][fi]
    print(genre_counts.most_common(10))
    return new_corpus

def is_actually_aux(w, parse):
    return False
    if w['dep'] == 'aux': return True
    if w['lemma'] == 'go':
        if next((True for wx in parse if w['i'] == wx['head.i'] and 
                 ((wx['dep'] == 'xcomp') or 
                  (wx['dep'] == 'advcl' and 
                   next((True for wy in parsed if wy['head.i'] == wx['i'] and wy['lemma'] == 'to'),False)))), False):
            return True
    return False

def get_mappable(parse):
    parenthetical_level = 0
    new_parse = []
    for w in parse:
        if w['text'] in '[(':
            parenthetical_level += 1
        if parenthetical_level == 0:
            new_parse.append(w)
        if w['text'] in ')]':
            parenthetical_level -= 1
        if parenthetical_level < 0:
            # print('  ' + ' '.join([w['text'] for w in parse]))
            parenthetical_level = 0
    return new_parse

def get_lexical(parse):
    return list(set(w['lemma'] for w in parse if (w['pos'] in good_pos and 
                                                  w['lemma'] not in excluded_lemmas and 
                                                  not is_actually_aux(w, parse))))