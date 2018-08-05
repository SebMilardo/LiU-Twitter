# -*- coding: utf-8 -*-
"""
Created on Sun May 26 03:55:52 2013

@author: Sebastiano Milardo

What characterizes a tweet that gets re-tweeted by many people? 
What kind of tweets generate many (new) followers?

"""

from __future__ import division, print_function
import json
import locale
import mapasync
import math
import nltk
import operator 
import os
import pickle
import random
import re
import sys
import time
import twitterhelper
import urllib
import urllib2
from collections import Counter
from HTMLParser import HTMLParser
from nltk.corpus import stopwords
from itertools import chain
from os.path import dirname, join
from prettytable import PrettyTable
from urllib import urlopen
from twitterhelper import get_tweets
from twitterhelper import get_users
from twitterhelper import DATA
from mapasync import map_async
from features import evaluate
from features import get_features
#==============================================================================
# 
#
#                      Tweet che vengono retwittati
#
#
#==============================================================================

#==============================================================================
# Loading...
#==============================================================================

queries = [line.strip() for line in open('queries.txt')]

STOP_WORDS = set(stopwords.words('english'))
RET = join(dirname(__file__), "retweeted")
SHF = join(dirname(__file__), "shuffled")

#==============================================================================
# Retrieving
#==============================================================================

if not os.path.exists(DATA) :

    os.mkdir(DATA)

if len(os.listdir(DATA))==0:
    
      print("Downloading Tweets...")    
      map_async(get_tweets, queries, threads=4)
      
else:
    print("Tweets have already been downloaded\n--- Loading...")

#==============================================================================
# for j in os.listdir(DATA):
#     tweets += pickle.load( open(join(DATA, j), "rb")) 
#==============================================================================

print("Tweets Loaded")


#==============================================================================
# Divisione Retwitted e Non | Estrazione Utenti
#==============================================================================


if not os.path.exists(RET) or len(os.listdir(RET))==0:

    os.mkdir(RET)
    print("Execute: python -u splitter...")              
     
else:
    print("Tweets have already been splitted\n--- Loading...")


users = pickle.load( open(join(RET, "Users.txt"), "rb")) 
print(" {} Unique Users ".format(len(users)))

if not os.path.exists(SHF) :

    os.mkdir(SHF)

if len(os.listdir(SHF))==0:
      print("Loadiing...")  
      retweeted = pickle.load( open(join(RET, "True.txt"), "rb")) 
      not_retweeted = pickle.load( open(join(RET, "False.txt"), "rb")) 
      print("Shuffling and saving...")    
      
      #tweets = retweeted + not_retweeted 
      tweets = retweeted
      print(len(tweets))
      random.shuffle(tweets)
      pickle.dump(tweets,open(join(SHF, "Shuffled.txt"),"wb"))
        
else:
    print("Tweets have already been shuffled\n--- Loading...")
    retweeted = pickle.load( open(join(RET, "True.txt"), "rb")) 
    not_retweeted = pickle.load( open(join(RET, "False.txt"), "rb")) 
      
    tweets = pickle.load( open(join(SHF, "Shuffled.txt"), "rb")) 

up = 0
down = 0
for tweet in retweeted:
    if tweet['punteggio'] >1:
        up +=1 
    else:
        down +=1

print(up)
print(down)

#==============================================================================
# Statistiche sui retwitted
#==============================================================================

# Most 20 retwitted
topRetweeted = sorted([(tweet['retweet_count'],
                 users[tweet['user_ret']]['followers_count'],
                 users[tweet['user_ret']]['screen_name'],
                 tweet['text'].replace("\n","")
                 ) for tweet in retweeted],reverse=True)[:20]
                 
pt = PrettyTable(field_names=['Count','Followers','Screen Name','Text'])
[ pt.add_row(row) for row in topRetweeted]
pt.max_width['Text'] = 160
pt.align= 'l'
print (pt)

# Most 20 retwitted / followers
topRetweetedF = sorted(
                [ (tweet['punteggio'],
                  users[tweet['user_ret']] ['followers_count'],
                  users[tweet['user_ret']] ['screen_name'],
                  tweet['text'].replace("\n",""))
                   for tweet in retweeted],reverse=True)[:20]
                 
pt = PrettyTable(field_names=['Count/Followers','Followers','Screen Name','Text'])
[ pt.add_row(row) for row in topRetweetedF]
pt.max_width['Text'] = 160
pt.align= 'l'
print (pt)


# Top 20 kill streak!
topRetweetedF = sorted(
                [ (tweet['lunghezza_serie'],
                  tweet['punteggio'],
                  users[tweet['user_ret']] ['screen_name'],
                  tweet['text'].replace("\n",""))
                   for tweet in retweeted],reverse=True)[:20]
                 
pt = PrettyTable(field_names=['Serie','Punteggio','Screen Name','Text'])
[ pt.add_row(row) for row in topRetweetedF]
pt.max_width['Text'] = 160
pt.align= 'l'
print (pt)


# Numero medio retweet
somma = 0;
for tweet in retweeted:
    somma += tweet['retweet_count']
    
print ("Average Retweet Count: {}".format(somma/len(retweeted)))


# Words
status_texts = [ status['text'].lower() for status in tweets ]

screen_names = [ user_mention['screen_name'].lower() 
                 for status in tweets
                     for user_mention in status['entities']['user_mentions'] 
                     if user_mention['screen_name'].lower() != "rt"]

hashtags = [ hashtag['text'].lower() 
                 for status in tweets
                     for hashtag in status['entities']['hashtags'] 
                     if hashtag['text'].lower() != "rt"]

                     
words = [ w.encode('ascii','ignore') for t in status_texts for w in nltk.word_tokenize(t) 
            if (w not in STOP_WORDS) and (w != "rt")]

links = []

for t in retweeted:
    try: 
        if (len(t['entities']['urls'])>0):
            for url in t['entities']['urls']:
                matchObj = re.search( r'//(.*?)/', url['expanded_url'], re.I)
                links.append(matchObj.group(1))

    except:
        continue

print(len(screen_names))
print(len(hashtags))
print(len(words))
print(len(links))

screen_names = Counter(screen_names).most_common()[:200]
hashtags = Counter(hashtags).most_common()[:100]
words = Counter(words).most_common()[20:420]
links = Counter(links).most_common()[:100]

print(screen_names)
print(hashtags)
print(words)
print(links)


#==============================================================================
# Allenamento su 24.000 non_ret/retwitted
#==============================================================================

featuresets = []  
                   
result=[
        [1],            #text
        [1,2],          #text + tweet
        [1,2,3],        #text + tweet + user
        [1,2,3,4],      #text + tweet + user + time
        [1,2,3,5],      #text + tweet + user + time2
        [1,3],          #text + user + time
        [1,3,4],        #text + user + time
        [1,3,5],        #text + user + time
        ]

threshold = int(len(tweets)*0.8)
 
print(len(tweets))
   
    # Training 
for i in range(len(result)):    
    featuresets = map_async(get_features,tweets,[screen_names,hashtags,words,links,users,result[i]])
    classifier = nltk.NaiveBayesClassifier.train(featuresets[:threshold])
    x = evaluate(classifier, featuresets[threshold:])
    classifier.show_most_informative_features(n=10)
    result[i] = x   
    
for i in result:
    print(i)    
   
# mostrare features più interessanti

#==============================================================================
# Prova su 6000 sconosciuti
#==============================================================================




#==============================================================================
# Risultati
#==============================================================================







#==============================================================================
# Allenamento 6.000 retwitted < ValoreMedio vs 6000 retwitted > ValoreMedio
#==============================================================================


# possibili features:
# - log numero followers
# - log numero status
# - has (lista hash)
# - has (lista nomi)
# - has (top 1000 parole più frequenti) 
# - has (top 1000 parole meno frequenti)
# - verified


# mostrare features più interessanti

#==============================================================================
# Prova su 3200 sconosciuti
#==============================================================================




#==============================================================================
# Risultati
#==============================================================================



#==============================================================================
# 
#
#                  Tweet che generano più nuovi followers
#
#
#==============================================================================

#==============================================================================
# Raccolta dati utenti
#==============================================================================





#==============================================================================
# Salvataggio
#==============================================================================

# mettere data e ora nel file

#==============================================================================
# Caricamento
#==============================================================================

#==============================================================================
# Confronto user con follower incrementati
#==============================================================================

# un bell'istogramma no?
# confronto iniziale finale 1 -> 10    1000 -> 1010

#==============================================================================
# Download completo timeline top 1000 user per incrememnto
#==============================================================================


#y = twitter_api.users.lookup(screen_name="JUSTKC__") #fino a 100 collegati con ","
#print (y)

# similarities? tf-idf???? conteggio @, conteggio # conteggio tweets #conteggio
# retweets