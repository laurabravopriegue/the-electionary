import commonfunctions as cf
import json
import os

directory = 'transcripts-10thDec'

# Produce a list of speakers
# So that we can find duplicate speaker names

# List all the files in the directory
filesList = os.listdir(directory)
# Create a list for all the objects imported to JSON to be added to
transcripts = []

# Go through each file, open it, and add its content to the list
for myFile in filesList:
    with open(os.path.join(directory, myFile), 'r') as f:
        # Here, the JSON is converted back to a Python object
        transcript = json.load(f)
    transcripts.append(transcript)

allSpeakers = []

# Go through each transcript
for transcript in transcripts:

    text_by_speakers = transcript['text_by_speakers']

    # Go through the speakers in the text organised by speaker
    speakers = []
    for speaker in text_by_speakers:
        speakers.append({'name': speaker['speaker']})

    # Loop through all speakers
    for speaker in speakers:
        # Loop through once again
        for speaker2 in speakers:
            # If they're not the same, but the difference is only one of case, add an identity.
            if speaker['name'] != speaker2['name'] and speaker['name'].lower() == speaker2['name'].lower():
                speaker['identity'] = speaker2['name']
                # Leave the for loop - we only need one identity for each.
                break
    myDict = {'date': transcript['date'], 'speakers': speakers, 'description': transcript['description']}
    allSpeakers.append(myDict)

with open('allSpeakers.json', 'w') as f:
    json.dump(allSpeakers, f)
