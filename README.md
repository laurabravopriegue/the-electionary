# the-electionary

## What this is

Software to download a series of debate transcripts and process them.

## How to use it

### Prerequisites

You must have scrapy installed before using this code.

To install scrapy, run the following in Terminal:

`pip install scrapy`

### Downloading the transcripts

Go to Terminal, and navigate to `debateScrape/debateScrape` in the terminal.

Then run `scrapy crawl urlfetch`. This fetches the list of URLs to download from.
Then run `scrapy crawl download`. This downloads all the HTML files containing the transcripts.
Be aware that this will take some time. The spider has been set to delay between downloading each file, to reduce server load for the host.
There should not be any need to do this more than once.
The HTML files will be stored in `debateScrape/debateScrape/html-files`. 
 
### Processing the transcripts

Now that you have all the HTML downloaded, you can now do whatever processing you like locally, which will be faster and will prevent unnecessary load on the host.
As a starting point, try running `transcript-postprocessor.py`.
This will produce a transcript for each candidate's speech in an individual debate in JSON format, located in the `debateScrape/debateScrape/transcripts` folder.

If you want to access the text or other attributes from these JSON files, you can use the following code:
(the information contained in the JSON file is detailed below)

~~~~
transcriptList = os.listdir('transcripts')

for item in transcriptList:
    with file(os.path.join('transcripts', item), 'r') as f:
        transcript = json.read(f)
        
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
    
    
    
    
    #WHATEVER YOU WANT TO DO WITH THE TEXT HERE.
    
~~~~
