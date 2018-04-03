# OER Commons - Nutch Web Crawler

## Crawl Process
Nutch Setup:
Just download and unzip the binaries.

Crawl:  ~/apache-nutch-1.14/bin/crawl -s url ist441_test 1
Merge Segments:  
~/apache-nutch-1.14/bin/nutch mergesegs mergedseg raw_data/segments/*
~/apache-nutch-1.14/bin/nutch dump -segment mergedseg/ -outputDir content_dump
