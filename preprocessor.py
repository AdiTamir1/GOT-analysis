#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 26 16:34:13 2018

@author: Nikie Jo Deocampo
"""
import json
import csv
import nltk
from nltk.tokenize import word_tokenize
import string
import re
import time
import pandas as pd


tweets_data = []
texts = []
words_sentiments = {}
ids = []
some_milby = []
print("===========================")
print("Starting Preprocess Function")
print("=========================== \n\n")

def getdata(dataurl):
    print("===========================")
    print("Retrieving TXT File")
    tweets_data_path = dataurl
    tweets_file = open(tweets_data_path, "r")
    for line in tweets_file:
        try:
            tweet = json.loads(line)
            tweets_data.append(tweet)
        except:
            continue
    print("===========================")
    print("Retrieving Successfull")
    print("=========================== \n \n")
    time.sleep(3)
    processdata()


def processdata():
    print("===========================")
    print("Recovering Data Teets")
    print("===========================")
    time.sleep(1)
    RE_EMOJI = re.compile('[\U00010000-\U0010ffff]', flags=re.UNICODE)
    for i in range(len(tweets_data)):
        text = tweets_data[i]['text']
        id_str = tweets_data[i]['id_str']
        text = RE_EMOJI.sub(r'', text)
        text = text.translate(str.maketrans('','',string.punctuation))
        texts.append(text)
        ids.append(id_str)
    print("===========================")
    print("Data Tweets Recovered")
    print("===========================\n\n")
    
    
    
def readdict(dataurl):
    print("===========================")
    print("Reading Dictionary")
    print("===========================")  
    with open(dataurl) as tsvfile:
      reader = csv.reader(tsvfile, delimiter='\t')
      for row in reader:
          words_sentiments[row[2]] = row[5]
    print("===========================")
    print("Dictionary Preparation Done")
    print("===========================\n\n")  
    addpolarity()

def addpolarity():  
    start_time = time.time()
    counter = 0
    print("===========================")
    print("Processing please wait...")
    print("===========================\n\n")
    
    
    
    for text in texts:
            tweet_token = text
            token = word_tokenize(tweet_token)
            sumnum = 0
            sum_word = 0
            for word in token:
                if word in words_sentiments:
                    sentiment = words_sentiments[word]
                    sum_word += 1

                    if sentiment == "positive":
                        sumnum += 1
                    elif sentiment == "negative":
                        sumnum += -1
                    else:
                        sumnum += 0
                 
            
            if sum_word != 0.0:
                sum_more = sumnum / sum_word
                sum_more_degree = sumnum / sum_word
                if sum_more >= 0.2:
                    sum_more = 1
   
                elif (sum_more < 0.2) and (sum_more > -0.5):
                    sum_more = 0
                   
                elif sum_more <= -0.5:
                    sum_more = -1
                   
                else:
                    print("****")
                    
                
            sum_var = []    
            varid = ids[counter]
            sum_var.append(varid)
            sum_var.append(sum_more)
            sum_var.append(sum_more_degree)
            some_milby.append(sum_var)
            counter += 1
            
    print("Processing time: ", round((time.time() - start_time),8), "Seconds \n\n")
    
    time.sleep(3)
        
    print("===========================")
    print("Processing Finish")
    print("===========================")
    
    
    savetoxlsx()
    
def savetoxlsx():
    df = pd.DataFrame(some_milby)
    df.to_excel('processed_data/output.xlsx', header=("id","sentiment", "degree"), index=False)
    
    
    #file = open("testfile_data.txt","w") 
    #file.write(some_milby) 
    #file.close() 
    
    print("===========================")
    print("Data Saved!")
    print("===========================") 
    

def runall():
    nltk.download('punkt')
    getdata('data/tweetdata.txt')
    readdict('data/dictionary.tsv')
    


runall()