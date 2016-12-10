import commonfunctions as cf
import json
import os
from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt

directory = 'transcripts-10thDec'

# Just an example of the kind of analysis that can be done
# This does a sentiment analysis on the text by year using TextBlob
# Then it creates a graph of that data (sentiment against time)

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

# Create lists for the years and the sentiment for each year.
years = []
sentiments = []

# Go through each transcript
for transcript in transcripts:

    # Get the date - converting the ISO date back into a datetime.date object
    date = cf.iso_to_datetime(transcript['date'])
    year = date.year
    years.append(year)

    # Create a string for all of the text in the debate
    allText = ""

    # Add all the text spoken by speakers to that string
    for speaker in transcript['text_by_speakers']:
        allText += (" " + speaker['text'])

    # Now create the TextBlob
    blob = TextBlob(allText)

    # Take the polarity from the TextBlob and add to the resultSentiments list
    sentiments.append(blob.sentiment.polarity)

# Get a unique list of the years
uniqueYears = list(set(years))

# Create a new list for the sentiments corresponding to each year.
uniqueSentiments = []

# For each unique year
for year in uniqueYears:
    # Create a list which will contain all sentiment values for a year
    sentimentsForYear = []

    # Go through all the different years, adding the sentiment to that list.
    for number in range(len(years)):
        if years[number] == year:
            sentimentsForYear.append(sentiments[number])

    # Take a simple mean of the sentiments of all texts in a given year.
    # Add this to the list uniqueSentiments, which is paired with the uniqueYears list.
    uniqueSentiments.append(np.mean(sentimentsForYear))

plt.plot(uniqueYears, uniqueSentiments, 'ro')
plt.xlabel('Year')
plt.ylabel('Sentiment')
plt.show()
