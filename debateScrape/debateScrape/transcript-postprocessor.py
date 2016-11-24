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
runForSample = False

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


# Function to extract the relevant text from a <p> element.
def extract_text_from_p(p_selector, tr_type, first=False):
    speaker_name = None

    if tr_type == 'bold' or tr_type == 'italic':
        if tr_type == 'bold':
            tag = 'b'
        elif tr_type == 'italic':
            tag = 'i'
        # If we're dealing with the first one, then we know where the <i> or <b> tag will be.
        if first:
            tag_range = [26, 29]
        else:
            tag_range = [3, 6]

        # Check if there is a relevant tag
        if p_selector.extract()[tag_range[0]:tag_range[1]] == "<" + tag + ">":

            # If there isn't anything after the italic element, don't include it
            # This deals with the problem subtitles, which are introducing false speakers.
            # See 2004-09-30 for an example
            if len(p_selector.xpath(".//text()").extract()) == 1 \
                    or p_selector.xpath(".//text()").extract()[1].replace(" ", "") == "":
                pass
            else:
                speaker_name = p_selector.xpath(".//" + tag + "/text()").extract()
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

    elif tr_type == 'capital':

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
        elif split_text[0].replace("Mc", "MC").replace("Mr", "MR").isupper():
            speaker_name = split_text[0]
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
    speaker_name = "unknown"

    # Create a new selector which selects the displaytext element.
    # This is for the first paragraph, which doesn't sit within <p> tags.
    first_element = transcript_selector.xpath("//span[@class='displaytext']")
    first_element = cf.list_to_item(first_element)

    # Need to pass the 'first' argument as True, because we're dealing with the first element.
    labelled_speech = extract_text_from_p(first_element, tr_type=transcript_type, first=True)
    if labelled_speech["speaker"] is not None:
        speaker_name = labelled_speech["speaker"]

    # Add the returned dict to the list of speeches.
    labelled_speeches.append(labelled_speech)

    # Generate a list of Selectors which are all <p> items
    p_selector_list = transcript_selector.xpath("//span[@class='displaytext']//p")

    # Loop through all these <p> Selectors
    for p_selector in p_selector_list:
        # Call the extraction function again
        labelled_speech = extract_text_from_p(p_selector, tr_type=transcript_type)

        # Once it's returned, take the speaker's name from the dict.
        new_speaker_name = labelled_speech["speaker"]

        if new_speaker_name is not None:
            if "APPLAUSE" in new_speaker_name:
                new_speaker_name = new_speaker_name.replace("(APPLAUSE)", "").replace("(APPLAUSE.)", "").replace(" ", "")
            if "(LAUGHTER)" in new_speaker_name:
                new_speaker_name = new_speaker_name.replace("(LAUGHTER)", "").replace(" ", "")
            if "(COMMERCIAL BREAK)" in new_speaker_name:
                new_speaker_name = new_speaker_name.replace("(COMMERCIAL BREAK)", "").replace(" ", "")

        # If the new speaker's name is valid, set the speaker name to that.
        # Otherwise, change what the labelled speech says.
        if new_speaker_name != "" and new_speaker_name is not None:
            speaker_name = new_speaker_name
        else:
            labelled_speech["speaker"] = speaker_name

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

    # CLASSIFY: Sort the transcripts out by the different ways that we will extract
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
            # At the moment, we're not doing anything with this type of transcript (n=9/147)
            return

    # Run the function for extracting the speeches from the transcript
    sentence_dicts = extract_transcript_selector(selector, transcript_type)

    # Identify all the speakers in the transcript
    speaker_list = []
    for sentence_dict in sentence_dicts:
        if sentence_dict["speaker"] is not None:
            sentence_dict["speaker"] = sentence_dict["speaker"].replace('/',' ')
        if sentence_dict["speaker"] is None:
            pass
        speaker_list.append(sentence_dict["speaker"])

    speaker_dicts = []

    for speaker in set(speaker_list):
        # Make a string for each speaker
        all_text_of_speaker = ""

        if speaker is None:
            speaker = "None"

        # Check all of the text to see if it belongs to that speaker and add it.
        for sentence_dict in sentence_dicts:
            if sentence_dict["speaker"] == speaker and sentence_dict["text"] is not None:
                all_text_of_speaker = all_text_of_speaker + " " + (sentence_dict["text"])

        # Finally, construct the dictionary that will be converted to a file.
        if speaker[-1] == " ":
            speaker = speaker[:-1]
        if speaker[-1] == ":":
            speaker = speaker[:-1]
        if speaker[-1] == ".":
            speaker = speaker[:-1]
        speaker_dict = {"speaker": speaker, "text": all_text_of_speaker}
        speaker_dicts.append(speaker_dict)

    file_dict = {"date": debate_date_iso, "description": debate_name, "speaker_dicts": speaker_dicts}
    filename = debate_date_iso + " " + debate_name + ".json"
    txt_filename = debate_date_iso + " " + debate_name + ".txt"

    # Write this to a file
    if filename is not None:
        with open(os.path.join(transcriptDir, filename), 'w') as f:
            json.dump(file_dict, f)
    else:
        raise Exception('A filename error occurred.')

for htmlFile in htmlList:
    process_html_file()
