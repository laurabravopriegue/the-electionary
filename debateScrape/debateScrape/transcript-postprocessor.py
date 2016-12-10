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

# Enter your working directories here:

# SAMPLE
if runForSample:
    htmlDirectory = 'html-output-sample'
    transcriptDir = 'transcripts-sample'

# NOT SAMPLE
else:
    htmlDirectory = 'html-output'
    transcriptDir = 'transcripts-10thDec'

# Make the directory to output to, if it doesn't exist already.
if transcriptDir not in os.listdir(os.curdir):
    os.mkdir(transcriptDir)

# List all the files in the directory.
htmlList = os.listdir(htmlDirectory)


# Function to extract the relevant text from a <p> element.
# The function takes a Selector for a <p> element.
# It returns a dict:
# labelled_speech = {"speaker": speaker_name, "text": sentence}
def extract_text_from_p(p_selector, tr_type, first_element=False):
    speaker_name = None

    # Set tag ranges appropriately depending on whether this is the first element
    # in the displaytext section.

    if first_element:
        xpath_address = "./text()"
        tag_range = [26, 29]
    else:
        xpath_address = ".//text()"
        tag_range = [3, 6]

    # This action just for transcripts with bold or italic elements
    if tr_type == 'bold' or tr_type == 'italic':
        # If there's a <p> tag immediately, just return False.
        # In this case, we return False, because the <p> elements are contained
        # in other elements later.
        if first_element and p_selector.extract()[tag_range[0]:tag_range[1]] == "<p>":
            return False

        # Set the tags correctly: bold tags have <b>, italic tags have <i>
        if tr_type == 'bold':
            tag = 'b'
        elif tr_type == 'italic':
            tag = 'i'

        # Check if there is a relevant tag, i.e. if the element starts with <b>
        if p_selector.extract()[tag_range[0]:tag_range[1]] == "<" + tag + ">":

            # If there isn't anything after the bold/italic element, don't include it
            # This deals with the problem subtitles, which are introducing false speakers.
            # e.g. <b>SOME TOPIC<b> is not a speaker.
            # See 2004-09-30 for an example

            # If there is no element after the bold/italic element or
            # If the element after the bold/italic element consists of spaces only
            if not (len(p_selector.xpath(".//text()").extract()) == 1 or
                            p_selector.xpath(".//text()").extract()[1].replace(" ", "") == ""):
                # Extract the speaker name from the text
                speaker_name = p_selector.xpath("./" + tag + "/text()").extract()
                # This returns a list, so need to take only the first element
                # We set this as the speaker name.
                speaker_name = cf.list_to_item(speaker_name)

            # Now we build the sentence. This is from the text in the selector.
            # first_string is being used to mark the speaker's name.
            sentence = ""
            first_string = True
            for words in p_selector.xpath(xpath_address).extract():
                # Don't include the first string. The first string is the speaker's name.
                # The only exception is when we're just in the displaytext part of the transcript.
                if first_string and not first_element:
                    first_string = False
                else:
                    # Add a space and then the words
                    sentence += (" " + words)

        # If there is no relevant tag - there is no speaker name.
        # Build the sentence in the same way. Don't change the speaker name.
        else:
            sentence = ""
            for words in p_selector.xpath(".//text()").extract():
                sentence += (" " + words)

    elif tr_type == 'upper':

        # Extract text from <p> element, make into one big string
        # We're not using the structure of the HTML here in a <p></p>
        text_list = p_selector.xpath(xpath_address).extract()
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

        # The only exception to uppercase speakers is Mc and MR, check these too
        elif split_text[0].replace("Mc", "MC").replace("Mr", "MR").isupper():
            speaker_name = split_text[0]
            if len(split_text) > 1:
                sentence = split_text[1]
            else:
                sentence = ""

        # If there isn't a speaker, all of the text is a sentence
        # (which will later be attributed to the previous speaker)
        else:
            sentence = all_text

    # Raise an exception if a malformed transcript type argument has been passed.
    # e.g. if tr_type = 'foo'
    else:
        print tr_type
        raise Exception('Classification error occurred.')

    # Tidy up the sentence. Remove colons from the beginning of the string.
    # Check the first character and if it's a space/colon,
    # remove it. This is done sequentially, so " : " will be removed.
    if sentence is not None and sentence != "":
        for character in [" ", " ", ":", " "]:
            if sentence[0] == character:
                sentence = sentence[1:]

            # If we have a blank sentence, break out of the loop.
            # This avoids errors where there are no characters for
            # us to look through.
            if sentence == "":
                break

    # Create a dict which contains the name of the speaker,
    # and the sentence which has been processed.
    # It is then returned back to the function which called this one.
    labelled_speech = {"speaker": speaker_name, "text": sentence}
    return labelled_speech


# Very large function to extract the text from a transcript selector.
# Takes a transcript Selector and returns a list,
# labelled_speeches, a list of labelled_speech dicts.
def extract_transcript_selector(transcript_selector, transcript_type):
    labelled_speeches = []
    speaker_name = "unknown"

    # First deal with the first paragraph, which doesn't sit in <p> tags.
    # Create a new selector which selects the displaytext element.
    first_element = transcript_selector.xpath("//span[@class='displaytext']")
    first_element = cf.list_to_item(first_element)

    # Call labelled_speech
    # Need to pass the 'first' argument as True, because we're dealing with the first element.
    labelled_speech = extract_text_from_p(first_element, tr_type=transcript_type, first_element=True)

    # Only do the following logic if labelled_speech actually returned something.
    # The function returns False if there wasn't any speech to return.
    if labelled_speech:
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

        # Tidy the speaker name
        if new_speaker_name is not None:
            if "APPLAUSE" in new_speaker_name:
                new_speaker_name = new_speaker_name.replace("(APPLAUSE)", "").replace("(APPLAUSE.)", "")
            if "(LAUGHTER)" in new_speaker_name:
                new_speaker_name = new_speaker_name.replace("(LAUGHTER)", "")
            if "(COMMERCIAL BREAK)" in new_speaker_name:
                new_speaker_name = new_speaker_name.replace("(COMMERCIAL BREAK)", "")

        # If the new speaker's name is valid, set the speaker name to that.
        # Otherwise, use the previous speaker's name.
        if new_speaker_name != "" and new_speaker_name is not None:
            speaker_name = new_speaker_name
        else:
            labelled_speech["speaker"] = speaker_name

        labelled_speeches.append(labelled_speech)

    return labelled_speeches


# Function to clean up the speaker's name.
def speaker_clean(speaker):
    # Change None to a string.
    if speaker is None or speaker == "":
        speaker = "None"
        return speaker

    # If the last character in the name of the speaker is a space, : or . then remove it
    for character in [" ", ":", "."]:
        if speaker[-1] == character:
            speaker = speaker[:-1]
        if speaker == "":
            return speaker

    return speaker


# Function to produce text files, for checking the work.
# NOT CURRENTLY BEING USED.
def create_text_file(debate_date_iso, debate_name, sentence_dicts):
    # Set the filename as the debate date, followed by a space, and the name.
    filename = debate_date_iso + " " + debate_name + ".txt"
    speaker = ""

    with open(os.path.join(transcriptDir, filename), 'w') as f:
        for sentence_dict in sentence_dicts:
            if sentence_dict['speaker'] != speaker:
                if sentence_dict['speaker'] is None:
                    sentence_dict['speaker'] = "None"
                f.writelines("\n\n")
                f.writelines(speaker_clean(sentence_dict['speaker']).encode('utf8'))
            f.writelines("\n    ")
            if sentence_dict['text'] is not None:
                f.writelines(sentence_dict['text'].encode('utf8'))
            speaker = sentence_dict['speaker']


# This function does all the work we want to do for a given HTML file.
# It takes a HTML filename, opens the file from the given directory,
# and does all the processing needed.
# It saves a result to a .json file in the output directory.
# The result is a JSON translation of:
# A dict, {"date": "", "description": "", "text_by_speakers": [],
#                  "transcript_type": ""}
# where text_by_speakers is a list of dicts, where each dict is:
# {"speaker": "", text: ""}

def process_html_file(html_file):
    # Read the HTML into a file object
    with file(os.path.join(htmlDirectory, html_file), 'r') as f:
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
    # If there are more than 50 bold elements, classify as "bold"
    if len(selector.xpath("//span[@class='displaytext']//b//text()").extract()) >= 50:
        transcript_type = "bold"

    # If there are more than 50 italic elements, classify as "italic"
    elif len(selector.xpath("//span[@class='displaytext']//i//text()").extract()) >= 50:
        transcript_type = "italic"

    # Otherwise, look at all the text. If there are more than 50 colons, classify it as "upper"
    # "upper" here refers to the fact that we will be checking if the speaker names are uppercase.
    else:
        text_from_all = selector.xpath("//span[@class='displaytext']//text()").extract()
        sentence = ""
        for text in text_from_all:
            sentence += text
        if sentence.count(":") >= 50:
            transcript_type = 'upper'
        else:
            # At the moment, we're not doing anything with this type of transcript (n=9/147)
            # So we don't return anything.
            return

    # Run the function for extracting the speeches from the transcript
    sentence_dicts = extract_transcript_selector(selector, transcript_type)

    # Uncomment the line below these comments if you want to output text files.
    # This can be useful for debugging how well it is working.
    # create_text_file(debate_date_iso, debate_name, sentence_dicts)

    # CODE TO OUTPUT JSON FILES FOR THE TRANSCRIPTS
    # Identify all the speakers in the transcript
    speaker_list = []
    for sentence_dict in sentence_dicts:
        if sentence_dict["speaker"] is not None:
            # Remove slashes - these cause problems when saving files, as they create directories
            sentence_dict["speaker"] = sentence_dict["speaker"].replace('/', ' ')

        speaker_list.append(sentence_dict["speaker"])

    # Set up a list which will contain a series of dicts, each of which
    # is consists of a speaker's name and everything they said.
    text_by_speakers = []

    candidates = None
    moderators = None

    # Go through all the speakers, not using duplicates
    for speaker in set(speaker_list):
        # Make a string for each speaker
        all_text_of_speaker = ""

        # Check all of the text to see if it belongs to that speaker and add it.
        for sentence_dict in sentence_dicts:
            if sentence_dict["speaker"] == speaker and sentence_dict["text"] is not None:
                all_text_of_speaker = all_text_of_speaker + " " + (sentence_dict["text"])

        # Clean the speaker's name
        speaker = speaker_clean(speaker)

        # Clean all text of the speaker, removing double spaces.
        all_text_of_speaker = all_text_of_speaker.replace("  ", " ")
        # remove first character if it's a space
        if len(all_text_of_speaker) > 0:
            if all_text_of_speaker[0] == " ":
                all_text_of_speaker = all_text_of_speaker[1:]
        # remove last character if it's a space
        if len(all_text_of_speaker) > 0:
            if all_text_of_speaker[-1] == " ":
                all_text_of_speaker = all_text_of_speaker[:-1]

        # If the speaker is 'candidates' (non-case-sensitive),
        # this is metadata and we should move it outside the main body.
        if speaker.lower() == "candidates":
            candidates_label = speaker
            candidates = all_text_of_speaker

        # Similarly for 'moderators'
        elif speaker.lower() == "moderators":
            moderators_label = speaker
            moderators = all_text_of_speaker

        else:
            speaker_dict = {"speaker": speaker, "text": all_text_of_speaker}
            text_by_speakers.append(speaker_dict)

    # Create a dictionary which will be written to a file
    file_dict = {"date": debate_date_iso, "description": debate_name, "text_by_speakers": text_by_speakers,
                 "transcript_type": transcript_type}

    # If there are candidate names, add these in to the metadata
    if candidates:
        file_dict[candidates_label] = candidates
    if moderators:
        file_dict[moderators_label] = moderators

    filename = debate_date_iso + " " + debate_name + ".json"

    # Write this to a file
    if filename is not None:
        with open(os.path.join(transcriptDir, filename), 'w') as f:
            json.dump(file_dict, f)
    else:
        raise Exception('A filename error occurred.')


for htmlFile in htmlList:
    process_html_file(htmlFile)
