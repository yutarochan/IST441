'''
Document Embedding - Training Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import sys
import nltk
import json
import random
import string
import logging
import numpy as np
from multiprocessing import Pool
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from gensim.models.doc2vec import TaggedDocument, Doc2Vec

# Logging
logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

# Application Parameters
DATAROOT_DIR = '/tmp/oer_rawtext/'
THREADS = 128

# Document Embedding Hyperparameters
VEC_DIM = 450
EPOCH = 50
WINDOW = 8
MIN_COUNT = 3

# Initialize NLTK Objects
stopwords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

# Set PRNG Seed
np.random.seed(2342234)

# Preprocessing Function
# TODO: Fix the preprocessing phase based on the structure of the json
def process(doc_id):
    text = open(DATAROOT_DIR + doc_id + '.txt', 'r').read()
    tokens = [stemmer.stem(t.lower()) for t in nltk.word_tokenize(text) if t.lower() not in stopwords and t.lower() not in string.punctuation]
    return LabeledDocs(tokens, doc_id)

# Document Object
class LabeledDocs(object):
    def __init__(self, tokens, tag):
        self.doc = TaggedDocument(words=tokens, tags=[tag])
        self.tag = tag

class DocList(object):
    def __init__(self, docs=None):
        if docs is None: self.docs = []
        else: self.docs = docs

    def append(self, doc_obj):
        self.docs.append(doc_obj)

    def toArray(self):
        docList_arr = []
        for d in self.docs: docList_arr.append(d.doc)
        return docList_arr

    def __iter__(self):
        for d in self.docs: yield d

    def size(self):
        return len(self.docs)

# Open Metadata File
print('LOADING DOCUMENT METADATA')
meta = json.loads(open('oer_metadata_redux.json', 'rb').read())
print('LOADED: ' + str(len(meta.keys())))

# Process Documents
print('BUIDLING DOCUMENT OBJECTS')
p = Pool(THREADS)
documents = DocList(p.map(process, list(meta.keys())))

# Train Document Vectors
model = Doc2Vec(vector_size = VEC_DIM, min_count = MIN_COUNT, epochs = EPOCH, workers = THREADS)
model.build_vocab(documents.toArray())

print('TRAINING DOCUMENT EMBEDDING')
# Shuffle Documents
train_docs = documents.toArray()
random.shuffle(train_docs)

# Train Model
model.train(train_docs, total_examples=model.corpus_count, epochs=model.epochs)
print('TRAIN COMPLETE')

# Persist Model
model.save('oer_d2v.pickle')
