'''
OER Commons - Seed Site Scraper
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import bs4
import time
import json
import requests

# Define Application Parameters
ROOT_DIR = '../data/'
ROOT_URL = 'https://www.oercommons.org'
BATCH_SIZE = 100
BUFFER_TIME = 60

def build_url(st_index, batch=100):
    return ROOT_URL + '/browse?batch_size=' + str(batch) + '&batch_start=' + str(st_index)

def extract_doc_count(headers):
    r = requests.get(ROOT_URL+'/browse', headers=headers)
    data = bs4.BeautifulSoup(r.text, 'html.parser')
    return int(data.findAll('span', {'class':'items-number'})[0].text[1:-1])

def extract_metadata(data):
    # Extract Primary Data
    uid = str(data.findAll("div", {"class": "item-title"})[0].a['href'].split('/')[-1])
    title = str(data.findAll("div", {"class": "item-title"})[0].text)
    rating = float(data.findAll("div", {"class": "stars"})[0]['data-rating-value'])

    abstract = None
    if len(data.findAll("div", {"class": "abstract-full"})) > 0:
        abstract = str(data.findAll("div", {"class": "abstract-full"})[0].p.text)

    # Extract Metadata
    meta = dict()
    metadata = bs4.BeautifulSoup(str(data.findAll('dl', {"class": "item-info"})), 'html.parser')
    for m in zip(metadata.find_all('dt'), metadata.find_all('dd')):
        meta[m[0].text.replace(':', '').strip()] = str(m[1].text)

    # Generate Dictionary
    result = { 'uid' : uid, 'title' : title, 'rating' : rating, 'meta' : meta }
    if abstract != None: result['abstract'] = abstract
    else: result['abstract'] = ''

    return result

seed_data = []

# Setup Request Headers
headers = requests.utils.default_headers()
headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

# Extract Document Count
doc_count = extract_doc_count(headers)
print('SEED SITE COUNT: ' + str(doc_count))

# Extract Seed UID
for i in range(0, doc_count, BATCH_SIZE):
    if i != 0 and i % 500 == 0: time.sleep(BUFFER_TIME) # Add time buffer for delay.

    print('PROCESSING: ' + build_url(i))
    r = requests.get(build_url(i), headers=headers)
    data = bs4.BeautifulSoup(r.text, 'html.parser')

    url_list = data.findAll('article')
    for j in range(len(url_list)):
        seed_data.append(extract_metadata(url_list[j]))

# Write to File
print('\n>> OUTPUT TO FILE')
output = open(ROOT_DIR + 'oer_seed.json', 'w')
output.write(json.dumps(seed_data))
output.close()
