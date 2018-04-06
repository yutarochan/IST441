'''
OER Commons - Statistical Analysis of Seed URL
Author: Yuya Jeremy Ong (yjo5006@psu.edu)
'''
from __future__ import print_function
import pprint
import tldextract
import collections
import seaborn as sns
import matplotlib.pyplot as plt
from urllib.parse import urlparse

# Application Parameters
ROOT_DIR = '../data/'

# Setup Pretty Printer
pp = pprint.PrettyPrinter(indent=4)

# Load Seed URL List
data = open(ROOT_DIR + 'oer_seed_url.csv', 'r').read().split('\n')
data = list(filter(lambda x: len(x) == 2, list(map(lambda x: x.split(','), data)))) # Split Commas & Collect URL

# Parse URL Schema
parsed_url = list(map(lambda x: urlparse(x[1]), data))

# Compute Scheme Distribution
scheme_dist = collections.Counter(list(map(lambda x: x.scheme, parsed_url)))
print('SCHEME DISTRIBUTION:')
pp.pprint(dict(scheme_dist))
print()

# Compute Base URL Distribution
baseurl_dist = collections.Counter(list(map(lambda x: tldextract.extract(x.netloc).domain, parsed_url)))
baseurl_hist = [baseurl_dist[x] for x in sorted(dict(baseurl_dist), reverse=True, key=baseurl_dist.__getitem__)]

print(baseurl_hist)

# Plot Distribution
plt.hist(baseurl_hist, log=True, bins=25)
plt.title('Seed URL Domain Frequency')
plt.xlabel('Value')
plt.ylabel('Frequency (Log-Scaled)')
plt.show()

# Compute Domain Suffix Distribution
dom_dist = collections.Counter(list(map(lambda x: tldextract.extract(x.netloc).suffix, parsed_url)))
pp.pprint(dom_dist)
