'''
OER Commons - Seed Site Seed URL Scraper

Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import bs4
import time
import json
import requests

# Application Parameters
ROOT_DIR = '../data/'
ROOT_URL = 'https://www.oercommons.org'
BUFFER_TIME = 60

def process_url(uid):
    req_url = ROOT_URL + '/courses/' + uid + '/view'

    # Setup Request Headers
    headers = requests.utils.default_headers()
    headers['User-Agent'] = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

    # Generate Request
    r = requests.get(req_url, headers=headers)
    data = bs4.BeautifulSoup(r.text, 'html.parser')

    # Extract URl
    url = None
    if len(data.findAll('a', {'class':'js-continue-redirect-button'})) > 0:
        url = data.findAll('a', {'class':'js-continue-redirect-button'})[0]['href']

    return url

# Open JSON File
data = json.loads(open(ROOT_DIR + 'oer_seed.json', 'r').read())

# Setup Data List
data_list = []

# Process Request
for i, d in enumerate(data):
    if i != 0 and i % 500 == 0:
        # Write to File
        print('\n>> OUTPUT TO FILE @ ' + str(i))
        output = open(ROOT_DIR + 'oer_seed_url.csv', 'a')
        for x in data_list:
            if x[1]: output.write(x[0] + ',' + x[1] + '\n')
        output.close()

        data_list = [] # Clear Queue
        time.sleep(BUFFER_TIME) # Add time buffer for delay.

    print('PROCESSING: ' + data[i]['uid'])
    data_list.append((data[i]['uid'], process_url(data[i]['uid'])))

# Write Remaining Data to File
print('\n>> OUTPUT TO FILE @ ' + str(i))
output = open(ROOT_DIR + 'oer_seed_url.csv', 'a')
for x in data_list:
    if x[1]: output.write(x[0] + ',' + x[1] + '\n')
output.close()
