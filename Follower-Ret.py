# -*- coding: utf-8 -*-
"""
Created on Sun May 26 20:28:41 2013

@author: Seby
"""
from __future__ import division, print_function
from os.path import dirname, join
#from twitter import TwitterHTTPError
import pickle
#import twitter
import time
import traceback
import sys
#import twitterhelper
#from twitterhelper import get_users
from mapasync import map_async
import pickle
from itertools import chain
import operator
import numpy as np
import pylab as P
import math
#import splitter


#retweeted = pickle.load( open("True.txt", "rb")) 
# not_retweeted = pickle.load( open("False.txt", "rb"))
RET = join(dirname(__file__), "retweeted")
print("carico...")
retweeted = pickle.load( open(join(RET, "True.txt"), "rb")) 
print("carico...")
users = pickle.load( open(join(RET, "Users.txt"), "rb")) 
# raw_input() 
#==============================================================================

#==============================================================================
#              ANALISI senza variazione derivate dal numero di followers
#==============================================================================


#==============================================================================
# lines = [line.strip() for line in open('keys.txt')]
# auth = twitter.oauth.OAuth(*lines)
# twitter_api = twitter.Twitter(domain='api.twitter.com', api_version='1.1', auth=auth)
# print("Twitter API Loaded")
#==============================================================================


print(len(retweeted))


fig = P.figure()
ax = fig.add_subplot(1,1,1)
ax.set_yscale('log')
ax.set_xscale('log')

fol_count = []
ret_count=[]
for tweet in retweeted:
    fol_count.append(users[tweet['user_ret']]['followers_count'])  
    ret_count.append(tweet['retweet_count'])
    
ax.plot(fol_count,ret_count,  "b.")

media = {}

for tweet in retweeted:
    followers_count = users[tweet['user_ret']]['followers_count']
    retweet = tweet['retweet_count']
    try:
        if media.has_key(round(math.log(followers_count,10),1)):
            media[round(math.log(followers_count,10),1)].append(retweet)
        else:
            media[round(math.log(followers_count,10),1)]=[]
            media[round(math.log(followers_count,10),1)].append(retweet)
    except:
        pass


divisivo = {}

    
for k in media.keys():
    print(sorted(media[k]))
    print([int(round(len(media[k])/2))])
    divisivo[k]= sorted(media[k])[int(round(len(media[k])/2))-1]

for k in media.keys():
    media[k]= sum(media[k])/len(media[k])

x = sorted(media.keys())
y = [media[x1] for x1 in x]
x2 = [math.pow(10,x1) for x1 in x]


ax.plot(x2,y,"g.")

y2 = [round((pow(5.5,(x1-2.5)))) for x1 in x]

ax.plot(x2,y2,color="red",lw=2)

y3 = [divisivo[x1] for x1 in x]

ax.plot(x2,y3,"k.")

P.legend(("tweets","average","model","half"),'lower right', shadow=True, fancybox=True)
P.title("Followers & Retweets")
P.ylabel("Retweets")
P.xlabel("Followers")

up      = 0
down    = 0

for r,f in zip(ret_count,fol_count):
     if ( round((pow(5.5,(math.log(f+1,10)-2.5)))) > r ):
         up += 1
     else:
         down += 1

P.show();

print(up)
print(down)

