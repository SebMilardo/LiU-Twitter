# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 18:35:10 2013

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
import collections
import os
import time
from features import to_epoch
from features import to_rt_score
import collections
import random

#retweeted = pickle.load( open("True.txt", "rb"))
# not_retweeted = pickle.load( open("False.txt", "rb"))
RET = join(dirname(__file__), "retweeted")
DATA = join(dirname(__file__), "tweets")



def split():

        users={}
        retweeted={}
        not_retweeted={}

        files = os.listdir(DATA)
            #fig = P.figure()
        for j in range(len(files)):
                print(".",end="")
                tweets = pickle.load( open(join(DATA, files[j]), "rb"))
                tweetAll={};
                
                    
                for i in range(len(tweets)):
                    print(".",end="")
                    try:
                        user_id = tweets[i]['user']['id']
                        users[user_id] = tweets[i]['user']
                        users[user_id]['created_at'] = to_epoch(users[user_id]['created_at']) 
                        
                        if tweets[i].has_key('retweeted_status') and tweets[i]['retweet_count']>0:
                            user_ret = tweets[i]['retweeted_status']['user']['id']
                            users[user_ret] = tweets[i]['retweeted_status']['user']
                            users[user_ret]['created_at'] = to_epoch(users[user_ret]['created_at']) 
                            t_id = tweets[i]['retweeted_status']['id']
                            tweets[i]['creato'] = to_epoch(tweets[i]['retweeted_status']['created_at'])
                            tweets[i]['punteggio'] = to_rt_score(tweets[i]['retweet_count'],tweets[i]['retweeted_status']['user']['followers_count'])
                            tweets[i]['user'] = user_id
                            tweets[i]['user_ret'] = user_ret
                            tweets[i]['retweeted_status']['user'] = user_ret                                                              
                        else:
                            t_id = tweets[i]['id']
                            tweets[i]['creato'] = to_epoch(tweets[i]['created_at'])
                            tweets[i]['punteggio'] = 0
                            tweets[i]['user'] = user_id
                                
                                
                        tweets[i]['posizione_serie'] = 0
                        tweets[i]['lunghezza_serie'] = 0
                        tweetAll[t_id]=tweets[i]
                        
                    except Exception, err:
                        print(Exception, err,"1")
                        continue
                    
                tweetAll=collections.OrderedDict(sorted(tweetAll.items()))

                tweets = sorted(tweetAll.items())
                for k in range(1,len(tweets)):
                    if ((tweets[k][1]['creato'] - tweets[k-1][1]['creato']) < 600):
                        tweets[k][1]['posizione_serie'] = tweets[k-1][1]['posizione_serie'] + 1
                        
                                
                    else:
                            tweets[k][1]['posizione_serie'] = 0  
                            lunghezza = tweets[k-1][1]['posizione_serie']+1
                            if (lunghezza > 1):
                                for j in range(int(lunghezza)):
                                    
                                    tweets[k-1-j][1]['posizione_serie']=((tweets[k-1-j][1]['posizione_serie'])*9/(lunghezza-1))+1
                                    tweets[k-1-j][1]['lunghezza_serie']=lunghezza
                                             
                
                lunghezza = tweets[k][1]['posizione_serie']+1
                if (lunghezza > 1):
                    for j in range(int(lunghezza)):
                                    
                        tweets[k-j][1]['posizione_serie']=((tweets[k-j][1]['posizione_serie'])*9/(lunghezza-1))+1
                        tweets[k-j][1]['lunghezza_serie']=lunghezza
                
                

                         
                for v in tweets:
                    print(v[1]['creato'],v[1]['posizione_serie'],v[1]['lunghezza_serie'],v[1]['text'].encode('ascii','ignore'))
                    if (v[1]['creato']>1369395008):                    
                        if v[1].has_key('retweeted_status') and v[1]['retweet_count']>0:
                                   retweeted[v[0]]=v[1]
                        else:
                                   not_retweeted[v[0]]=v[1]                        

        print(len(retweeted.keys()))
        print(len(not_retweeted.keys()))
        print(len(users.keys()))

        retweeted = retweeted.values()
        not_retweeted = not_retweeted.values()

        retweeted =  [
        retweeted[i] for i in random.sample(xrange(len(retweeted)), 7600)] #e se invece di random togliessi quelli con pochi followers?
        not_retweeted = [
        not_retweeted[i] for i in random.sample(xrange(len(not_retweeted)), 7600)]

        pickle.dump(retweeted,open(join(RET, "True.txt"),"wb"))
        pickle.dump(not_retweeted,open(join(RET, "False.txt"),"wb"))
        pickle.dump(users,open(join(RET,"Users.txt"),"wb"))                   
                                                        
split()                   
              