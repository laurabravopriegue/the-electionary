# the-electionary

## IMPORTANT - DISCLAIMER

This software is released under the MIT license. However, the transcripts collected by the program are subject to copyright and it is your sole responsibility to ensure that you use any data collected during your use of the software in accordance with the law.

## What this is

Software to download a series of debate transcripts from the [American Presidency Project](http://presidency.ucsb.edu/debates.php) and process them.

## Branches

The `master` branch doesn't do any collection of the transcripts from the website - it only does processing.

If you want to download the HTML files from the website, clone the `download-files` branch instead. That also includes all the processing code.

## How to use it

### Prerequisites for downloading the HTML files

You must have `scrapy` installed before using this code.

To install `scrapy`, run the following in Terminal:

`pip install scrapy`

(this applies only to macOS/OS X - look at the documentation for other platforms).

### Downloading the transcripts

Go to Terminal, and navigate to `debateScrape/debateScrape` in the terminal.

Then run `scrapy crawl urlfetch`. This fetches the list of URLs to download from.

Then run `scrapy crawl download`. This downloads all the HTML files containing the transcripts.

Be aware that this will take some time. The spider has been set to delay between downloading each file, to reduce server load for the host.
**There should not be any need to do this more than once.**

The HTML files will be stored in `debateScrape/debateScrape/html-files`. 
 
### Processing the transcripts

Now that you have all the HTML downloaded, you can now do any processing from the local files, which will be much faster and will prevent unnecessary load on the host. You can now clone `master` if you like.
As a starting point, try running `transcript-postprocessor.py`.
This will produce a transcript for each candidate's speech in an individual debate in JSON format, located in the `debateScrape/debateScrape/transcripts` folder.

If you want to access the text or other attributes from these JSON files, you can use the following code:

~~~~
transcriptList = os.listdir('transcripts')

for item in transcriptList:
    with open(os.path.join('transcripts', item), 'r') as f:
        transcript = json.load(f)
        
    # For full text of the speech of one person in the transcript:    
    text = transcript['text']
    
    # For the speaker's name:
    speaker = transcript['speaker']
    
    # For a description of the debate:
    # (e.g. "Democratic Candidates Debate in Brooklyn, New York")
    description = transcript['description']
    
    # For the date of the debate:
    # (e.g. "2016-04-14")
    debateDate = transcript['date']    
    
    #Insert your code here to deal with the data...
    
~~~~
