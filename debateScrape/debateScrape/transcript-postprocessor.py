# Transcript Processor
# Reads the HTML files from debateScrape/debateScrape/html-files
# Separates debate transcripts into what was said by each speaker
# Produces JSON output with text and metadata

# Revised strategy:
# Categorise the transcripts into different types.
# If there are <b> or <i> tags in the transcript, use those.
# If there are uppercase statements followed by colons, use those.
from __future__ import division

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
    htmlDirectory = 'html-output'
    transcriptDir = 'transcripts-23-11-2016'

# Make the directory to output to, if it doesn't exist already.
if transcriptDir not in os.listdir(os.curdir):
    os.mkdir(transcriptDir)

# List all the files in the directory.
htmlList = os.listdir(htmlDirectory)


# htmlList = ["December 9, 2007 Republican Presidential Candidates Debate at the University of Miami.html"]


# Function to extract the relevant text from a <p> element.
def extract_text_from_p(p_selector, default_speaker_name, tr_type, first=False):
    # Use the default speaker name as passed to function.
    speaker_name = default_speaker_name

    if tr_type == 'b' or tr_type == 'i':
        # If we're dealing with the first one, then we know where the <i> or <b> tag will be.
        if first:
            tag_range = [26, 29]
        else:
            tag_range = [3, 6]

        # Check if there is a relevant tag
        if p_selector.extract()[tag_range[0]:tag_range[1]] == "<" + tr_type + ">":

            # If there isn't anything after the italic element, don't include it
            # This deals with the problem subtitles, which are introducing false speakers.
            # See 2004-09-30 for an example
            if len(p_selector.xpath(".//text()").extract()) == 1 \
                    or p_selector.xpath(".//text()").extract()[1].replace(" ", "") == "":
                pass
            else:
                speaker_name = p_selector.xpath(".//" + tr_type + "/text()").extract()
                speaker_name = cf.list_to_item(speaker_name)

            # Now we build the sentence. This is from the text in the selector.
            sentence = ""
            first_time = True
            for words in p_selector.xpath(".//text()").extract():
                # Don't include the first element. The first element is the speaker's name.
                if first_time:
                    first_time = False
                else:
                    sentence += (" " + words)

        # If there is no relevant tag - there is no speaker name.
        # Build the sentence in the same way. Don't change the speaker name.
        else:
            sentence = ""
            for words in p_selector.xpath(".//text()").extract():
                sentence += (" " + words)

    elif tr_type == 'u':

        # Extract text from <p> elements, make into one big string
        text_list = p_selector.xpath(".//text()").extract()
        all_text = ""
        for text in text_list:
            all_text += text

        # Split at colons
        split_text = all_text.split(":", 1)
        # Returns a list with at most two elements

        # If the first element of the list is uppercase, this is the speaker.
        if split_text[0].isupper():
            speaker_name = split_text[0]
            # If there's a sentence to go with it, use it.
            if len(split_text) > 1:
                sentence = split_text[1]
            else:
                sentence = ""
        else:
            sentence = all_text

    # Raise an exception if a malformed transcript type argument has been passed.
    else:
        raise Exception('Classification error occurred.')

    labelled_speech = {"speaker": speaker_name, "text": sentence}
    return labelled_speech


# Very large function to extract the text from a transcript selector.
def extract_transcript_selector(transcript_selector, transcript_type):
    labelled_speeches = []

    if transcript_type == 'italic':
        transcript_type = 'i'
    if transcript_type == 'bold':
        transcript_type = 'b'
    if transcript_type == 'capital':
        transcript_type = 'u'

    # Create a new selector which selects the displaytext element.
    # This is for the first paragraph, which doesn't sit within <p> tags.
    first_element = transcript_selector.xpath("//span[@class='displaytext']")
    first_element = cf.list_to_item(first_element)

    speaker_name = "unknown"

    # Need to pass the 'first' argument as True, because we're dealing with the first element.
    labelled_speech = extract_text_from_p(first_element, speaker_name, tr_type=transcript_type, first=True)

    # Once it's returned, take the speaker's name from the dict.
    speaker_name = labelled_speech["speaker"]

    # Add the returned dict to the list of speeches.
    labelled_speeches.append(labelled_speech)

    # Generate a list of Selectors which are all <p> items
    p_selector_list = transcript_selector.xpath("//span[@class='displaytext']//p")

    # Loop through all these <p> Selectors
    for p_selector in p_selector_list:
        # Call the extraction function again
        labelled_speech = extract_text_from_p(p_selector, speaker_name, tr_type=transcript_type)
        speaker_name = labelled_speech["speaker"]
        labelled_speeches.append(labelled_speech)

    return labelled_speeches


def process_html_file():
    # Read the HTML into a file object
    with file(os.path.join(htmlDirectory, htmlFile), 'r') as f:
        html_text = f.read()

    # Remove </b><b> and </i><i> pairs
    html_text = html_text.replace("</b><b>", "")
    html_text = html_text.replace("</i><i>", "")

    # Instantiate TranscriptSelector
    # TranscriptSelector inherits from scrapy.Selector and adds some functions of our own.
    # selector is the object we will be working on from here onwards.
    selector = cf.TranscriptSelector(text=html_text)

    # METADATA: Get the name and date of the debate
    debate_name = selector.get_debate_name()
    debate_date_iso = selector.get_debate_date()

    # DATA

    # Sort the transcripts out by the different ways that we will extract
    # information from them
    if len(selector.xpath("//span[@class='displaytext']//b//text()").extract()) >= 50:
        transcript_type = "bold"

    elif len(selector.xpath("//span[@class='displaytext']//i//text()").extract()) >= 50:
        transcript_type = "italic"

    else:
        text_from_all = selector.xpath("//span[@class='displaytext']//text()").extract()
        sentence = ""
        for text in text_from_all:
            sentence += text
        if sentence.count(":") >= 50:
            transcript_type = 'capital'
        else:
            # At the moment, we're not doing anything with this type of transcript (9/147)
            return

    sentence_dicts = extract_transcript_selector(selector, transcript_type)

    # Identify all the speakers in the transcript
    speaker_list = []

    for sentenceDict in sentence_dicts:
        speaker_list.append(sentenceDict["speaker"])

    for speaker in set(speaker_list):
        # Make a string for each speaker
        all_text_of_speaker = ""

        if speaker is None:
            speaker = "None"
        speaker = speaker.replace("/", "")

        # Check all of the text to see if it belongs to that speaker and add it.
        filename = None
        txt_filename = None
        for sentenceDict in sentence_dicts:
            if sentenceDict["speaker"] == speaker and sentenceDict["text"] is not None:
                all_text_of_speaker = all_text_of_speaker + " " + (sentenceDict["text"])
                filename = speaker + " " + debate_date_iso + ".json"
                txt_filename = speaker + " " + debate_date_iso + ".txt"

        # Finally, construct the dictionary that will be converted to a file.
        file_dict = {"speaker": speaker, "date": debate_date_iso, "description": debate_name,
                     "text": all_text_of_speaker}

        # Write this to a file
        if filename is not None:
            with open(os.path.join(transcriptDir, filename), 'w') as f:
                json.dump(file_dict, f)
        else:
            raise Exception('A filename error occurred.')

        if txt_filename is not None:
            with open(os.path.join(transcriptDir, txt_filename), 'w') as f:
                f.write(all_text_of_speaker.encode('utf8'))
        else:
            raise Exception('A filename error occurred.')


for htmlFile in htmlList:
    process_html_file()
