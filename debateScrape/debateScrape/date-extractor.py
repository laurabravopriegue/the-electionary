# Reasonably simple program which extracts the date to make for easy file sorting.

import os
from scrapy.http import HtmlResponse
from scrapy.selector import HtmlXPathSelector
import datetime as dt

runForSample = True
runForSample = False

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

    # Instantiate scrapy's HtmlResponse class with that text
    # This is so that scrapy will be happy processing the file
    response = HtmlResponse(url="", body=response)

    # Again we're instantiating another scrapy subclass.
    # This allows us to use all scrapy's selection methods.
    hxs = HtmlXPathSelector(response)

    #   METADATA
    # First, let's get some metadata.
    # We're using scrapy Selectors to pull out the date from the HTML.
    date = hxs.select("//span[@class='docdate']/text()").extract()

    # Unfortunately, we're returned a list with one element, so let's sort that.
    for date in date:
        debateDate = date
        break

    # Same thing for the name of the debate, also listed.
    name = hxs.select("//span[@class='paperstitle']/text()").extract()
    for name in name:
        debateName = name
        break

    # The date is not in a useful format, so let's change that.
    # Some uninteresting code to do that is below.

    debateDate = debateDate.split()
    wordMonth = debateDate[0]

    debateDate[1] = debateDate[1].split(',')
    dayNo = int(debateDate[1][0])
    yearNo = int(debateDate[2])

    months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October",
              "November", "December"]
    monthNo = int(months.index(wordMonth) + 1)

    # Finally we use the datetime library to store the date as a date object, and then convert that to an ISO format date.
    debateDateISO = dt.date(yearNo, monthNo, dayNo)
    debateDateISO = debateDateISO.isoformat()

    newFileName = debateDateISO + " " + debateName

    with file(os.path.join(outputDirectory, newFileName + '.html'), 'w') as f:
        f.write(response.body)