# -*- coding: utf-8 -*-
"""
Created on Sat Jun  1 17:00:41 2013

@author: Seby
"""

from __future__ import division, print_function
import pickle
from os.path import dirname, join
import matplotlib.pyplot as P
import numpy as np
import re
from collections import Counter



RET = join(dirname(__file__), "retweeted")
SHF = join(dirname(__file__), "shuffled")

retweeted = pickle.load( open(join(RET, "True.txt"), "rb")) 
not_retweeted = pickle.load( open(join(RET, "False.txt"), "rb")) 
users = pickle.load( open(join(RET, "Users.txt"), "rb")) 
shuffled = pickle.load( open(join(SHF, "Shuffled.txt"), "rb"))

print(" {} Unique Retweeted Tweets".format(len(retweeted)))
print(" {} Non Retweeted Tweets".format(len(not_retweeted)))
print(" {} Unique Users ".format(len(users)))


#==============================================================================
# Time
#==============================================================================
dates=[]
for u in shuffled:
    if (u['creato']>1369395008):
        dates.append(u['creato'])
    
print(len(dates))
print(max(dates))
fig = P.figure()
P.title("Dates (All)")
ax = fig.add_subplot(1,1,1)
ax.set_yscale('log')
ax.hist(dates, range(1369395008,1369595008,3600))
P.ylabel("n. of tweets")
P.xlabel("Date")
P.show()

#==============================================================================
# retweeted
#==============================================================================

retweets_counts=[]

followers=[]

punteggi=[]

serie=[]

lserie=[]

links=[]

for t in retweeted:
    try: 
        if (len(t['entities']['urls'])>0):
            for url in t['entities']['urls']:
                matchObj = re.search( r'//(.*?)/', url['expanded_url'], re.I)
                links.append(matchObj.group(1))
                
        retweets_counts.append(t['retweet_count'])
        followers.append(users[t['user_ret']]['followers_count'])
        punteggi.append(t['punteggio'])
        serie.append(t['posizione_serie'])
        lserie.append(t['lunghezza_serie'])
    except:
        continue
valori = [pow(10,x) for x in np.arange(0,9,0.2)]    



links = Counter(links).most_common()[:300]

print(links)

fig = P.figure()
P.title("Retweets")
ax = fig.add_subplot(1,1,1)
ax.set_xscale('log')
ax.hist(retweets_counts, bins=[pow(10,x) for x in np.arange(0,5,0.2)]  )
P.ylabel("Count")
P.xlabel("Retweets")
P.show()


fig = P.figure()
P.title("Followers (R)")
ax = fig.add_subplot(1,1,1)
ax.set_xscale('log')
ax.hist(followers, bins=[pow(10,x) for x in np.arange(0,9,0.2)]    )
P.ylabel("Count")
P.xlabel("Followers")
P.show()



fig = P.figure()
ax = fig.add_subplot(1,1,1)
ax.set_yscale('log')
ax.hist(punteggi, bins=np.arange(0,10,0.1))
P.show()




fig = P.figure()
P.title("Posizione Serie (R)")
ax = fig.add_subplot(1,1,1)
ax.hist(serie, bins=np.arange(0,1,0.01))
P.show()


fig = P.figure()
P.title("Lunghezza Serie (R)")
ax = fig.add_subplot(1,1,1)
ax.hist(lserie, bins=(range(0,1400,100)))
P.show()


#==============================================================================
# not retweeted
#==============================================================================

followers=[]
for t in not_retweeted:
    followers.append(users[t['user']]['followers_count'])
print(len(followers))
fig = P.figure()
P.title("Followers (NR)")
ax = fig.add_subplot(1,1,1)
ax.set_xscale('log')
ax.hist(followers, bins=[pow(10,x) for x in np.arange(0,9,0.2)]    )
P.ylabel("Count")
P.xlabel("Followers")
P.show()


#==============================================================================
# All
#==============================================================================
raw_input()
followers=[]
for u in users.values():
    followers.append(u['followers_count'])
print(len(followers))


fig = P.figure()
P.title("Followers (All)")
ax = fig.add_subplot(1,1,1)
ax.set_xscale('log')
ax.hist(followers, bins=[pow(10,x) for x in np.arange(0,9,0.2)]    )
P.ylabel("Count")
P.xlabel("Followers")
P.show()

