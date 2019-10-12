from __future__ import unicode_literals
import spacy, time
nlp = spacy.load('en_core_web_md')

def score_sentences(first, second):
    doc1 = nlp(first)
    doc2 = nlp(second)
    doc1_nostop = nlp(' '.join([str(t) for t in doc1 if not t.is_stop]))
    doc2_nostop = nlp(' '.join([str(t) for t in doc2 if not t.is_stop]))

    # print(doc1.similarity(doc2))
    return doc1_nostop.similarity(doc2_nostop)


