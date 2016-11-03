# the-electionary

## How to use the scrapy programs

In order to use `url-fetcher.py`, you first need a file `url.txt` in the directory `debateScrape/debateScrape`
This file simply needs the starting URL.
You also need another file, `urls.json`.
This file should take the following form:

`{"start_urls":["url1", "url2"],"allowed_domains":"domain"}`

In order to run the file, you must first install scrapy (Google for documentation if you're not sure how.)

Then, to run the programs, navigate to `debateScrape/debateScrape` in the terminal.

Then run `scrapy crawl geoffrey` followed by `scrapy crawl craig`.

The results will arrive in `debateScrape/debateScrape/transcripts`.