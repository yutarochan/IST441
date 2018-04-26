'''
OER Commons - Count Vectorizer
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import json
import nltk
import string
from scipy.spatial import KDTree
from multiprocessing import Pool
from nltk.corpus import stopwords
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer

# Application Parameters
DATAROOT_DIR = '/tmp/oer_rawtext/'
THREADS = 256
VECTOR_DIM = 2048

# Initialize NLTK Objects
stopwords = set(stopwords.words('english'))
stemmer = SnowballStemmer("english")

# Preprocessing Function
# TODO: Fix the preprocessing phase based on the structure of the json

def load_doc(doc_id):
    return str(open(DATAROOT_DIR + doc_id + '.txt', 'r').read())

def preprocess(text):    
    return [t.lower() for t in nltk.word_tokenize(text) if t.lower() not in stopwords and t.lower() not in string.punctuation]

# Open Metadata File
print('LOADING DOCUMENT METADATA')
meta = json.loads(open('oer_metadata_redux.json', 'rb').read())
print('LOADED: ' + str(len(meta.keys())))

# Load Documents into Memory
print('LOADING DOCUMENTS INTO MEMORY')
p = Pool(THREADS)
documents = list(p.map(load_doc, list(meta.keys())))

# Initialize Vectorizer
print('VECTORIZING TOKENS')
vec = TfidfVectorizer(max_features=2048)
X = vec.fit_transform(documents)

print('MAPPING TO INDEX HASH VALUE')
data = list(zip(meta.keys(), X.tolist()))
print(data)

'''
print('BUILDING KDTREE')
kdt = KDTree(data)

print('BUILD QUERY VECTOR')
q_vec = vec.transform([preprocess('japanese economy')])

print(kdt.query(q_vec))
'''
