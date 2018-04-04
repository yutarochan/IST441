# OER Commons - Nutch Web Crawler

## Nutch Crawler Configuration
Download the latest vesrion of Nutch version 1.14
[https://www.apache.org/dist/nutch/1.14/](https://www.apache.org/dist/nutch/1.14/)

## Crawl Process
The following process was used  to crawl and generate dumps of the crawl data.
### Crawling
    ~/apache-nutch-1.14/bin/crawl -s url ist441_test 1

### Merge Segments
    ~/apache-nutch-1.14/bin/nutch mergesegs mergedseg raw_data/segments/*
    ~/apache-nutch-1.14/bin/nutch dump -segment mergedseg/ -outputDir content_dump
