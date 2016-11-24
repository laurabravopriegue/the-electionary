import commonfunctions as cf
import json
import os
from textblob import TextBlob
import numpy as np
import matplotlib.pyplot as plt

filesList = os.listdir('transcripts-23-11-2016')
print filesList

filesListJSON = []
for myFile in filesList:
    if '.json' in myFile:
        filesListJSON.append(myFile)

transcripts = []

for myFile in filesListJSON:
    with open(os.path.join('transcripts-23-11-2016', myFile), 'r') as f:
        transcript = json.load(f)
    transcripts.append(transcript)

resultYears = []
resultSentiments = []

for transcript in transcripts:
    allText = ""
    date = cf.iso_to_datetime(transcript['date'])
    resultYear = date.year
    resultYears.append(resultYear)
    for speaker in transcript['speaker_dicts']:
        allText += (" " + speaker['text'])
    blob = TextBlob(allText)
    resultSentiments.append(blob.sentiment.polarity)

resultYearSet = set(resultYears)
resultYearSet = list(resultYearSet)
resultYearSentiments = []

for resultYear in resultYearSet:
    resultYearList = []
    for number in range(len(resultYears)):
        if resultYears[number] == resultYear:
            resultYearList.append(resultSentiments[number])
    resultYearSentiments.append(np.mean(resultYearList))

plt.plot(resultYearSet, resultYearSentiments, 'ro')
plt.xlabel('Year')
plt.ylabel('Sentiment')
plt.show()
