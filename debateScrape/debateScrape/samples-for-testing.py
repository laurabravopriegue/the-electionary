import os
import numpy as np
import shutil
filesList = os.listdir('transcripts-for-checking')

for x in filesList:
    shutil.copy(os.path.join('transcripts-for-checking',x),'transcripts-random')
    html = x[:-3] + "html"
    shutil.copy(os.path.join('html-output',html),'transcripts-random')
    randInt = str(int(np.random.randint(1000,9999)))
    os.rename(os.path.join('transcripts-random', x), os.path.join('transcripts-random', (randInt + ".txt")))
    os.rename(os.path.join('transcripts-random', html), os.path.join('transcripts-random', (randInt + ".html")))