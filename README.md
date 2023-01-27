# HUDOC Downloader

The point of this program is to provide an easy way to download European Court of Human Rights cases of a search. The script provides an example for the downloads a particular search of cases (see below), but can be edited to work with other searches. 

<img src="img/search.PNG" height=500 width=1200>

The objective of this script is enable reproducible research. Automated downloading helps by ensuring that:
* Overcoming the time limitations that manual downloads involve.
* Ensuring there is a code record of how cases where downloaded, to ensure a lack of selection bias or human error, and a print out of failed downloads.

Automation uses selenium and chromedriver. Make sure you have a chromedriver version that is compatible with your chrome version.

The output of this notebook puts the cases in txt and html format. 

You will need to run this from the command line, pointing to a yaml file with the flag -y. The yaml file **must** contain
* your search (copied from the address bar after querying HUDOC)
* the directory for storing html files
* the directory for storing txt files
* the directory where chromedriver is to be found.

Please follow example.yml and modify to suit your needs.

<img src="img/example.PNG" height=500 width=800>


### added value:

Although mass datasets with "all" the ECHR cases are available, these datasets might have many missing cases leading to unknown degrees of lost data. Downloading of a search leads to smaller datasets, but more insight into how many cases downloaed versus failed to download.

Also, it is not technically scraping, for those with concerns on the legality of that.

### TODO

* add flag to run headless or not
* get a written report of donwloaded, non-downloaded files
* figure out how to upload to pypi
