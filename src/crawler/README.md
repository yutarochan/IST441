# OER Commons Crawler
This section of the repository documents the process for crawling the seed sites
from OER Commons, along with the setup process and the entire automation process.

## Installation
Binaries for HTTrack can be installed through
[http://www.httrack.com/page/2/en/index.html](http://www.httrack.com/page/2/en/index.html).

Linux binaries for HTTrack can be downloaded and compiled through following the
installation instructions provided by the documentation.

## Crawler Command
The execution per process will be using the following command:

    httrack <urls> -O "<raw data location>"

From this command we utilize the following parameters:

`-O` - Prevent site from asking for a password credential

`-rN` - Number of depth to download the site.

`-cN` - Number of multiple connections.

`-p1` - Priority Mode: save only non html files

`-D` - Traverses only downwards the link hierarchy of a site

`-i` - Skips mirroring prompt as displayed by HTTrack

`-q` - Quiet Mode; Does not display anything on-screen

## HTTrack Process Orchestrator
To facilitate and scale our crawl operations, we wanted to utilize multiple
processes to take advantage of the hardware for faster processing.
The `httrack_crawler.py` script in this repository helps to orchestrate multiple
instances of HTTrack and leverages the multi-core processor of the CPU to increase
overall throughput.

Below we provide some key parameters that users should set:
