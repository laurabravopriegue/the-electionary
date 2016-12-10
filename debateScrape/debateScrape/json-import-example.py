import commonfunctions as cf
import json
import os

directory = 'transcripts-10thDec'

# Example to demonstrate opening JSON files
# And starting to process them

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

# From now on, we don't have to worry about JSON objects.

# Create lists for the years and the sentiment for each year.
years = []
sentiments = []

# Go through each transcript
for transcript in transcripts:

    # Get the date of the debate - converting the ISO date back into a datetime.date object
    date = cf.iso_to_datetime(transcript['date'])

    # Uncomment any of the attributes you'd like from the debate

    # year = date.year
    # month = date.month
    # day = date.day

    # Create a string for all of the text in the debate
    allText = ""

    # This is probably the main bit that is interesting for analysis purposes

    text_by_speakers = transcript['text_by_speakers']

    # Go through the speakers in the text organised by speaker
    for speaker in text_by_speakers:
        # speaker['speaker'] is the speaker's name
        print speaker['speaker']
        # speaker['text'] is everything that speaker said
        print speaker['text']