# CorefCoherence

To use this code, there are 2 steps.

## Step 1: Run coreference resolution
There are details in the Dependencies section on the coref model I used. You can use another as long as the output matches the defined format.

I've included a file (e2e_gen_coref.py) that you can copy into the e2e-coref folder. If you run it ($ python e2e_gen_coref.py) it should run the model on a sample sentence. You can simply change this file to load and run your text.

**OUTPUT** : You'll want to store the output as a dictionary of string (some id for the speaker) to list of reference chains (these are output by the e2e-coref model). I have include a sample (sample_data.pickle).

Roughly, the format will be as follows:  
{"speaker0": [  
&nbsp;&nbsp;&nbsp;&nbsp;['bob', 'he'],  
&nbsp;&nbsp;&nbsp;&nbsp;['my friends', 'they']  
],  
"speaker1": [  
&nbsp;&nbsp;&nbsp;&nbsp;['the door', 'it'],  
&nbsp;&nbsp;&nbsp;&nbsp;['i', 'i']  
]}

## Step 2: Run coref.py to output counts of ambiguous pronouns

First, try running the current file as is:   
$ python coref.py

This will load the sample_data and print the ambiguous pronouns per speaker. Nothing is printed if the ambiguous pronoun count is zero.

In coref.py, replace "sample_data.pickle" with your own text data which you generate in step 1 and run the same way.


## Dependencies:
Download an off the shelf coreference resolution model
Any should work but below is the one I used:

https://github.com/kentonl/e2e-coref

I have provided a sample program (e2e_gen_coref.py) to run the e2e-coref code after you have
followed all of their install steps. It just makes it easier to insert
you own text data.
**See last two lines for where to insert your own data**
