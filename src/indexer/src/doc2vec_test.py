'''
Document Embedding - Testing Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import string
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec
from nltk.stem.snowball import SnowballStemmer

# Load model
model = Doc2Vec.load('oer_d2v.pickle')

def preprocess(text):
    return [stemmer.stem(t.lower()) for t in nltk.word_tokenize(text) if t.lower() not in stopwords and t.lower() not in string.punctuation]

def query(keywords):
    tokens = preprocess(keywords)
    new_vector = model.infer_vector(tokens)
    return model.docvecs.most_similar([new_vector])
