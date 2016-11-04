# Transcript Processor
# Reads the HTML files from debateScrape/debateScrape/html-files
# Separates debate transcripts into what was said by each speaker
# Produces JSON output with text and metadata

from scrapy.selector import HtmlXPathSelector
import json
import os
from scrapy.http import HtmlResponse
import datetime as dt

# List all the files in the directory
htmlDirectory = 'html-files'
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
    # Some uninteresting code to take that out is below.

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

    #   DATA

    # Extract all of the text, and put it all in one long string, allText.
    titles = hxs.select("//span[@class='displaytext']//text()").extract()
    allText = ""
    for title in titles:
        allText = allText + " " + title

    # Now split the text at the colons, which indicate speaker changes (mainly!)
    # splitText is a list of strings; the last word in each string is the speaker of the following string.
    splitText = allText.split(":")

    # sentenceWords will be a new list of lists of strings, which are each individual words.
    sentenceWords = []
    for sentence in splitText:
        sentenceWords.append(sentence.split())

    # We tuple the sentences and the overall list, because there were mutability issues later.
    for sentence in sentenceWords:
        tuple(sentence)
    tuple(sentenceWords)

    # sentenceDicts will be a list of dictionaries, which have two keys:
    # text, whose value is a string containing the sentence
    # speaker, whose value is a string which is the word.

    sentenceDicts = []
    defaultSpeaker = ""

    # N.B. if you're changing this to a function later, you might have to watch for variable scope.
    for index in range(len(sentenceWords) - 1):

        # Our point of interest will be the second element onwards.
        sentenceNo = index + 1

        sentenceDict = {}

        # Adding the speaker's name from the last word in the previous sentence
        # Speaker names are always listed in upper case, so we can disregard it otherwise.
        # Speaker name will be stored as a field in the dictionary.

        if sentenceWords[sentenceNo - 1][-1].isupper():
            sentenceDict["speaker"] = sentenceWords[sentenceNo - 1][-1]
            speaker = sentenceDict["speaker"]
        else:
            sentenceDict["speaker"] = speaker

        # Make a new list, delete the last element from the list if it's uppercase
        # (removing the names from the text)
        newSentence = list(sentenceWords[sentenceNo])
        if newSentence[-1].isupper():
            del newSentence[-1]

        # Now we need to reconstruct the sentences. (At the moment we just have a list of words)
        newSentenceString = ""
        # If this isn't the first time that we're going through the loop, add a space each time.
        for word in newSentence:
            if newSentenceString != "":
                newSentenceString = newSentenceString + " " + word
            else:
                newSentenceString += word

        # Finally, we can put this sentence into the dictionary.
        sentenceDict["text"] = newSentenceString

        # Now append the dictionary to the list of sentences.
        sentenceDicts.append(sentenceDict)

    # Identify all the speakers in the transcript, without duplicates
    speakerList = []

    for sentenceDict in sentenceDicts:
        speakerList.append(sentenceDict["speaker"])
    set(speakerList)

    for speaker in speakerList:
        # Make a string for each speaker
        allTextOfSpeaker = ""

        # Check all of the text to see if it belongs to that speaker and add it.
        for sentenceDict in sentenceDicts:
            if sentenceDict["speaker"] == speaker:
                allTextOfSpeaker = allTextOfSpeaker + " " + (sentenceDict["text"])
                fileName = speaker + " " + debateDateISO + ".json"

        # Finally, construct the dictionary that will be converted to a file.
        fileDict = {"speaker": speaker, "date": debateDateISO, "description": debateName, "text": allTextOfSpeaker}

        # Write this to a file
        with open(os.path.join('transcripts2', fileName), 'w') as f:
            json.dump(fileDict, f)
