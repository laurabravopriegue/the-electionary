# Transcript Processor
# Reads the HTML files from debateScrape/debateScrape/html-files
# Separates debate transcripts into what was said by each speaker
# Produces JSON output with text and metadata

# Revised strategy:
# Categorise the transcripts into different types.
# If there are <b> tags in the transcript, use those.
# These are the most reliable.
# If there are uppercase statements followed by colons, use those.
# Only then resort to more difficult approaches.

from scrapy.selector import HtmlXPathSelector
import json
import os
from scrapy.http import HtmlResponse
import datetime as dt

# By default, the program runs only for a sample of files.
# To change this, change the following to False.
runForSample = True
# runForSample = False

if runForSample:
    htmlDirectory = 'html-files-sample'
    transcriptDir = 'transcripts-sample'
else:
    htmlDirectory = 'html-files'
    transcriptDir = 'transcripts-new'

# Make the directory to output to, if it doesn't exist already.
if transcriptDir not in os.listdir(os.curdir):
    os.mkdir(transcriptDir)

# List all the files in the directory
htmlList = os.listdir(htmlDirectory)


def listToItem(anyList):
    for item in anyList:
        return item


def getDebateDate(hxs):
    date = hxs.select("//span[@class='docdate']/text()").extract()

    debateDate = listToItem(date)

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

    # Finally we use the datetime library to store the date as a date object
    # and then convert that to an ISO format date.
    debateDate = dt.date(yearNo, monthNo, dayNo)
    return debateDate.isoformat()


def textExtract(hxs, transcriptType):
    labelledSpeeches = []
    if transcriptType == 'bold':
        transcriptDisplayText = hxs.select("//span[@class='displaytext']").extract()
        print transcriptDisplayText

        # Perhaps convert this to XPath Methods?
        # There must be a way...
        for transcriptDisplayText in transcriptDisplayText:
            transcriptDisplayText = transcriptDisplayText
        splitTdtByBs = transcriptDisplayText.split("<b>")
        print splitTdtByBs

        i = 0

        for splitTdtByB in splitTdtByBs:
            i += 1

            splitTdtBwithin = splitTdtByB.split("</b>")
            print "splitTdtBwithin:" + str(splitTdtBwithin)

            splitTdtBwithinResponses = []

            for item in splitTdtBwithin:
                splitTdtBwithinResponses.append(HtmlXPathSelector(HtmlResponse(url="", body=item, encoding='utf8')))

            if len(splitTdtBwithin) > 1:

                date2 = splitTdtBwithinResponses[0].select("//text()").extract()
                speakerName = listToItem(date2)
                speakerName = speakerName.replace(":", "")

                print "speakerName: " + speakerName

                date2 = splitTdtBwithinResponses[1].select("//text()").extract()
                pieceOfSpeech = ""
                for item in date2:
                    pieceOfSpeech += (" " + item)
                print "pieceOfSpeech: " + pieceOfSpeech

            else:
                speakerName = "unknown"
                pieceOfSpeech = splitTdtBwithinResponses[0].select("//text()").extract()
                pieceOfSpeech = listToItem(pieceOfSpeech)
                print "unknown:" + str(splitTdtBwithin[0])
                print "unknown:" + str(pieceOfSpeech)

            labelledSpeech = {"speaker": speakerName, "text": pieceOfSpeech}
            labelledSpeeches.append(labelledSpeech)
        print labelledSpeeches
        return labelledSpeeches


for htmlFile in htmlList:

    # Read the HTML into a file object
    with file(os.path.join(htmlDirectory, htmlFile), 'r') as f:
        response = f.read()

    # Instantiate scrapy's HtmlResponse class with that text
    # This is so that scrapy will be happy processing the file
    # FOR SOME REASON, THIS REPLACE METHOD IS NOT WORKING HERE. I DON'T KNOW WHY.
    response = response.replace("</b><b>","")

    print response
    if htmlFile == 'April 26, 2007 Democratic Presidential Candidates Debate at South Carolina State University in Orangeburg.html':
        break
    response = HtmlResponse(url="", body=response)

    # Again we're instantiating another scrapy subclass.
    # This allows us to use all scrapy's selection methods.
    hxs = HtmlXPathSelector(response)

    # METADATA

    # Get the name of the debate
    name = hxs.select("//span[@class='paperstitle']/text()").extract()
    for name in name:
        debateName = name
        break

    # Get the date of the debate

    debateDateISO = getDebateDate(hxs)

    #   DATA

    textFromBoldElements = hxs.select("//span[@class='displaytext']//b//text()").extract()
    if textFromBoldElements != "":
        transcriptType = "bold"
        sentenceDicts = textExtract(hxs, transcriptType)

    # Identify all the speakers in the transcript, without duplicates
    speakerList = []

    for sentenceDict in sentenceDicts:
        speakerList.append(sentenceDict["speaker"])
    print set(speakerList)

    for speaker in set(speakerList):
        # Make a string for each speaker
        allTextOfSpeaker = ""

        # Check all of the text to see if it belongs to that speaker and add it.
        for sentenceDict in sentenceDicts:
            if sentenceDict["speaker"] == speaker and sentenceDict["text"] is not None:
                allTextOfSpeaker = allTextOfSpeaker + " " + (sentenceDict["text"])
                fileName = speaker + " " + debateDateISO + ".json"

        # Finally, construct the dictionary that will be converted to a file.
        fileDict = {"speaker": speaker, "date": debateDateISO, "description": debateName, "text": allTextOfSpeaker}

        # Write this to a file
        with open(os.path.join(transcriptDir, fileName), 'w') as f:
            json.dump(fileDict, f)