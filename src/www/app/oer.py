'''
Document Embedding - Query Routine
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import nltk
import json
import string
from nltk.corpus import stopwords
from gensim.models.doc2vec import Doc2Vec
from nltk.stem.snowball import SnowballStemmer

# Application Parameters
MODEL_ROOT = 'app/model/'

# Initialize NLTK Objects
stopwords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

# Load Document Metadata
print('LOADING DOCUMENT METADATA')
meta = json.loads(open(MODEL_ROOT + 'oer_metadata_redux.json', 'rb').read())
print('LOADED: ' + str(len(meta.keys())))

# Load model
model = Doc2Vec.load(MODEL_ROOT + 'oer_d2v.pickle')

def preprocess(text):
    return [t.lower() for t in nltk.word_tokenize(text) if t.lower() not in stopwords and t.lower() not in string.punctuation]

def query(keywords, n=20, thresh=0.2):
    # Preprocess Query
    tokens = preprocess(keywords)
    new_vector = model.infer_vector(tokens)

    # Perform Search
    results = model.docvecs.most_similar([new_vector], topn=n)
    
    # Filter Cosine Similarity Threshold
    results = list(filter(lambda x: x[1] > thresh, results))

    # Extract and Map to Metadata
    res_set = [meta[r[0]] for r in results]

    return res_set