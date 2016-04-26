# media-crawl
crawlers for various polish internet media

Currently used (available categories):
* gazeta.pl (Polska, Polityka, Świat)
* naszdziennik.pl (Polska, Świat, Ekonomia)
* se.pl (Polska, Polityka, Świat)

To install:

* clone project
* cd to root directory
* type: pip install -r requirements.txt

Requirements:

* Python 2.7
* Scrapy 1.0.5 (requires C++ compiler)

To run:

* cd to root directory
* type: scrapy crawl _GazetaPl | NaszDziennik | SE_ -o output_filename.json
