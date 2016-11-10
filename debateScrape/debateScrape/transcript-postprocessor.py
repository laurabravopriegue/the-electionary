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

from scrapy.selector import Selector
import json
import os
import commonfunctions as cf

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

# List all the files in the directory.
htmlList = os.listdir(htmlDirectory)


# Very large function to extract the text from a selector.
def text_extract(selector, transcript_type):
    labelled_speeches = []

    # This is only able to deal with those transcripts where the speaker names
    # are contained within <b> elements.
    if transcript_type == 'bold':

        # First we just need to take out the displaytext part.
        transcript_displaytext = selector.xpath("//span[@class='displaytext']").extract()
        transcript_displaytext = cf.list_to_item(transcript_displaytext)

        # Split at the <b> tags.
        transcript_text = transcript_displaytext.split("<b>")

        for text_segment in transcript_text:

            # Split again at the closing </b> tags (we need to remove these)
            text_segment = text_segment.split("</b>")

            text_segment_list = []

            # Need to convert back into a Selector, so we can use XPath methods again.
            for item in text_segment:
                text_segment_list.append(Selector(text=item))

            # Only proceed if we have two elements in this list: these will be name and sentence.
            if len(text_segment_list) > 1:

                # Extract the speaker's name and reformat.
                speaker_name = text_segment_list[0].xpath("//text()").extract()
                speaker_name = cf.list_to_item(speaker_name)
                speaker_name = speaker_name.replace(":", "")

                # Extract all the other text which is not in <b> tags
                # This is a list; there is a lot in other tags, such as <p> etc.
                sentence_list = text_segment_list[1].xpath("//text()").extract()
                sentence = ""
                for item in sentence_list:
                    # Adding a space here, because <br> and <p> tags don't always have spaces
                    # which would otherwise concatenate words together.
                    sentence += (" " + item)

            else:

                # If we don't have anything in <b> tags, list as unknown speaker.
                speaker_name = "unknown"
                sentence = ""
                for item in sentence_list:
                    sentence += (" " + item)

            # Return a dictionary of return speaker-text pairs.
            labelled_speech = {"speaker": speaker_name, "text": sentence}
            labelled_speeches.append(labelled_speech)

        return labelled_speeches


for htmlFile in htmlList:

    # Read the HTML into a file object
    with file(os.path.join(htmlDirectory, htmlFile), 'r') as f:
        htmlText = f.read()

    # Remove </b><b> pairs
    htmlText = htmlText.replace("</b><b>", "")

    # Instantiate TranscriptSelector
    # TranscriptSelector inherits from scrapy.Selector and adds some functions of our own.
    # selector is a useful object that we can make various function calls from.
    selector = cf.TranscriptSelector(text=htmlText)

    # METADATA: Get the name and date of the debate
    debateName = selector.get_debate_name()
    debateDateISO = selector.get_debate_date()

    # DATA

    textFromBoldElements = selector.xpath("//span[@class='displaytext']//b//text()").extract()
    if textFromBoldElements != "":
        transcriptType = "bold"
        sentenceDicts = text_extract(selector, transcriptType)

    # Identify all the speakers in the transcript, without duplicates
    speakerList = []

    for sentenceDict in sentenceDicts:
        speakerList.append(sentenceDict["speaker"])

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
