from __future__ import division
import commonfunctions as cf
import json
import os
import nltk
wnl = nltk.WordNetLemmatizer()
from string import punctuation 
from string import digits
import urllib


directory = 'transcripts-10thDec'


#This code creates a graph that shows the frequency of different words over time
#In this case ive chosen as an example the words: racist, immigration, lation and america 
#Things to be changed: the X axis shoud represent years 

# List all the files in the directory
filesList = os.listdir(directory)
# Create a list for all the objects imported to JSON to be added to
transcripts = []


#import positive and negative lists
#create empty lists for both 

files=['negative.txt','positive.txt']

path='http://www.unc.edu/~ncaren/haphazard/'
for file_name in files:
    urllib.urlretrieve(path+file_name,file_name)
    
pos_words = open("positive.txt").read()
positive_words=pos_words.split('\n')
positive_counts=[]

neg_words = open('negative.txt').read()
negative_words=neg_words.split('\n')
negative_counts=[]

# Go through each file, open it, and add its content to the list
for myFile in filesList:
    with open(os.path.join(directory, myFile), 'r') as f:

        # Here, the JSON is converted back to a Python object
        transcript = json.load(f)
    transcripts.append(transcript)

# Create lists for the years and the sentiment for each year.
years = []
length = []

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
    
    	#Removing punctuation, digits
    	#Splitting text into words 
    	#Removing short words and sufixes 	
    	for p in list (punctuation):
    		allText = allText.replace(p,'')
    		
    	for k in list(digits): 
    		allText = allText.replace(k,'')  
    	
    	words = allText.split()
    	
    	
    	long_words = [w for w in words if len(w) > 3]
    
	listofwords = [wnl.lemmatize(t) for t in long_words]
	
	text = nltk.Text(listofwords)
	
	
#This creates the graph with the words in the parentheses 

text.dispersion_plot(["immigration", "latino", "america", "racist"])
