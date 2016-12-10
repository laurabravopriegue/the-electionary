import nltk
import os

textlist = []

for filename in os.listdir('transcripts-random'):
    if '.txt' in filename:
        with open(os.path.join('transcripts-random', filename), 'r') as f:
            f = f.read()
            textlist.append(f)

for myItem in textlist:
    tokens = nltk.word_tokenize(myItem)
    simple_text = nltk.Text(tokens)
    print simple_text.collocations()