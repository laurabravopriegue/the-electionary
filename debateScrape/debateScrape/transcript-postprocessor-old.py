# 1988-10-13 BAD
# 2004-10-13 OK, but also title issues
# 1996-10-16 as A
# 2012-10-16 as A
# 2012-10-03 as A
# 2004-10-05 BAD
# 1996-10-06 as A
# 2004-10-08 as A
# 1980-09-21 BAD
# 2004-09-30 as A

# This is only able to deal with those transcripts where the speaker names
# are contained within <b> elements.
if transcript_type == 'bold':
    tag = "b"
    closeTag = "</b>"

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
            if speaker_name is not None:
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
            sentence_list = text_segment_list[0].xpath("//text()").extract()
            for item in sentence_list:
                sentence += (" " + item)

        # Return a dictionary of return speaker-text pairs.
        labelled_speech = {"speaker": speaker_name, "text": sentence}
        labelled_speeches.append(labelled_speech)

    return labelled_speeches

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
speaker = "unknown"

# N.B. if you're changing this to a function later, you might have to watch for variable scope.
for index in range(len(sentenceWords) - 1):

    # Our point of interest will be the second element onwards.
    sentenceNo = index + 1

    sentenceDict = {}

    # Adding the speaker's name from the last word in the previous sentence
    # Speaker names are always listed in upper case, so we can disregard it otherwise.
    # Speaker name will be stored as a field in the dictionary.

    previousSentence = sentenceWords[sentenceNo - 1]
    speakerName = []

    # Going through all the items in the previous sentence.
    for word in previousSentence[::-1]:
        includeWord = True
        if word == "PARTICIPANTS":
            speakerName.append(word)
            break

        if word.isdigit():
            includeWord = False
            break

        if word.islower():
            # Don't include any solely lowercase words.
            includeWord = False
            break

        else:
            for mark in [".", "?", "!", "(", ")", "[", "]"]:
                if mark in word:
                    includeWord = False

        if includeWord:
            speakerName.append(word)
        else:
            print word + " was excluded"

    speakerString = ""
    if speakerName == []:
        speakerString = sentenceDicts[-1]["speaker"]
    else:
        number = 0
        for word in speakerName[::-1]:
            number += 1
            if number == 1:
                speakerString += word
            else:
                speakerString += (" " + word)
    sentenceDict["speaker"] = speakerString
    print speakerString

    # if previousSentence[-1][0].isupper():
    #
    #     if len(previousSentence) >= 2:
    #         if previousSentence[-2][0].isupper() and "." not in previousSentence[-2]\
    #                 and "?" not in previousSentence[-2] and "!" not in previousSentence[-2]\
    #                 and ")" not in previousSentence[-2]:
    #         # "Q" is appropriate.
    #         # "News Candidates" is something just to be disregarded.
    #         # "South Carolina" is disregard
    #         #
    #             sentenceDict["speaker"] = previousSentence[-2] + " " + previousSentence [-1]
    #         else:
    #             sentenceDict["speaker"] = sentenceWords[sentenceNo - 1][-1]
    #     else:
    #         sentenceDict["speaker"] = sentenceWords[sentenceNo - 1][-1]
    #     speaker = sentenceDict["speaker"]
    # else:
    #     sentenceDict["speaker"] = speaker

    # Make a new list, delete the last element from the list if it's uppercase
    # (removing the names from the text)
    newSentence = list(sentenceWords[sentenceNo])
    # FLAG: THIS IS SERIOUSLY WRONG AND NEEDS RECTIFYING
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
    break