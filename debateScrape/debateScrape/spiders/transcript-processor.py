# Transcript Processor
# Downloads from a specified list of URLs
# Separates debate transcripts into what was said by each speaker

from scrapy.spider import BaseSpider
from scrapy.selector import HtmlXPathSelector
import json
import os

class MySpider(BaseSpider):
    name = "craig"

    with file('urls.json', 'r') as f:
        startData = json.load(f)

    allowed_domains = startData["allowed_domains"]
    start_urls = startData["start_urls"]

    def parse(self, response):
        hxs = HtmlXPathSelector(response)

        date = hxs.select("//span[@class='docdate']/text()").extract()
        for date in date:
            debateName = date
            break

        # Select all <p> elements in response
        # This thing extracts all of the text from the page
        titles = hxs.select("//span[@class='displaytext']//text()").extract()
        #print titles

        allText = ""
        for title in titles:
            allText = allText + " " + title

        # allText is the full text of the debate
        # print allText

        splitText = allText.split(":")
        #print splitText

        # splitText is a list of strings. The last word in each string is the name of the speaker of the next string.

        # sentenceWords will be a new list of lists of strings, which are each individual words.
        sentenceWords = []
        for sentence in splitText:
            sentenceWords.append(sentence.split())

        for sentence in sentenceWords:
            tuple(sentence)

        tuple(sentenceWords)

        # sentenceDicts will be a list of dictionaries, which have two keys:
        # text, whose value is a string containing the sentence
        # speaker, whose value is a string which is the word.

        sentenceDicts = []
        defaultSpeaker = ""

        #N.B. if you're changing this to a function later, you might have to watch for variable scope.
        for index in range(len(sentenceWords)-1):

            # Our point of interest will be the second element onwards.
            sentenceNo = index + 1

            #Adding the speaker's name from the last word in the previous sentence
            sentenceDict= {}

            if sentenceWords[sentenceNo-1][-1].isupper():
                sentenceDict["speaker"] = sentenceWords[sentenceNo-1][-1]
                speaker = sentenceDict["speaker"]
            else:
                sentenceDict["speaker"] = speaker

            #Make a new list, delete the last element from the list
            newSentence = list(sentenceWords[sentenceNo])
            if newSentence[-1].isupper():
                del newSentence[-1]

            newSentenceString = ""
            # If this isn't the first time that we're going through the loop, add a space
            for word in newSentence:
                if newSentenceString != "":
                    newSentenceString = newSentenceString + " " + word
                else:
                    newSentenceString += word

            #Finally, we can put this sentence into the dictionary.
            sentenceDict["text"] = newSentenceString
            sentenceDicts.append(sentenceDict)

        # print sentenceDicts

        speakerList = []

        for sentenceDict in sentenceDicts:
            speakerList.append(sentenceDict["speaker"])

        # Remove duplicates from the list of speakers
        set(speakerList)

        for speaker in speakerList:
            # Make a string for each speaker
            allTextOfSpeaker = ""
            for sentenceDict in sentenceDicts:
                if sentenceDict["speaker"] == speaker:
                    allTextOfSpeaker = allTextOfSpeaker + " " + (sentenceDict["text"])
                    fileName = speaker + " " + debateName + ".txt"

            # Write this to a file
            with open(os.path.join('transcripts', fileName), 'w') as f:
                f.write(allTextOfSpeaker.encode('utf8'))