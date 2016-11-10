# Reasonably simple program which extracts the date to make for easy file sorting.

import os
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
import commonfunctions as cf

runForSample = True
# runForSample = False

if runForSample:
    htmlDirectory = 'html-files-sample'
    outputDirectory = 'html-output-sample'
    transcriptDir = 'transcripts-sample'
else:
    htmlDirectory = 'html-files'
    outputDirectory = 'html-output'
    transcriptDir = 'transcripts-new'

if outputDirectory not in os.listdir(os.curdir):
    os.mkdir(outputDirectory)

htmlList = os.listdir(htmlDirectory)

for htmlFile in htmlList:

    # Read the HTML into a file object
    with file(os.path.join(htmlDirectory, htmlFile), 'r') as f:
        response = f.read()

    # Instantiate TranscriptSelector with that response
    selector = cf.TranscriptSelector(text=response)

    # Fetch the debate date and debate name from that instance
    debateDateISO = selector.get_debate_date()
    debateName = selector.get_debate_name()

    newFileName = debateDateISO + " " + debateName

    with file(os.path.join(outputDirectory, newFileName + '.html'), 'w') as f:
        f.write(response)