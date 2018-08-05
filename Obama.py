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
from features import to_epoch
import matplotlib.pyplot as P
import numpy as np


DATA = join(dirname(__file__), "tweets")

print("carico...")
tweets = pickle.load( open(join(DATA, "Obama.txt"), "rb")) 



times = []
values = []


for i in range(len(tweets)):
    if tweets[i].has_key('retweeted_status') and tweets[i]['retweet_count']>0:
        tweets[i]['creato'] = to_epoch(tweets[i]['retweeted_status']['created_at'])
    else :
        tweets[i]['creato'] = to_epoch(tweets[i]['created_at'])

    times.append(tweets[i]['creato']-1369516168)
    values.append(tweets[i]['retweet_count'])

tweets = sorted(tweets, key=lambda k: k['creato']) 




fig = P.figure()
P.title("Obama related tweets")
ax = fig.add_subplot(1,1,1)

ax.hist(times, bins=np.arange(40000,60000,60)    )
P.ylabel("Tweets")
P.xlabel("Time(s)")
P.show()


fig = P.figure()
P.title("Obama related tweets")
ax = fig.add_subplot(1,1,1)
ax.plot(times,values,  "b.")
ax.grid(True, which="both")
ax.set_xscale("log")
ax.set_yscale("log")

P.ylabel("Retweets")
P.xlabel("Time(s)")
P.show()

