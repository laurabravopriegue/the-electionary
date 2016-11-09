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