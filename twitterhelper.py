from __future__ import division, print_function
from os.path import dirname, join
from twitter import TwitterHTTPError
import pickle
import twitter
import time
import traceback
import sys

timestamp = int(time.time())
DATA = join(dirname(__file__), "tweets")

lines = [line.strip() for line in open('keys.txt')]
auth = twitter.oauth.OAuth(*lines)
twitter_api = twitter.Twitter(domain='api.twitter.com', api_version='1.1', auth=auth)
print("Twitter API Loaded")

#==============================================================================
# retrieve max 1500 tweets about a specific query
#==============================================================================

def get_tweets(q,options=None):
        cont = True   
        while(cont):
            try:
                search_results = twitter_api.search.tweets(q=q, count=100, lang="en")
                reset = search_results.rate_limit_reset
                remaining = search_results.rate_limit_remaining
                print(reset)
                print(remaining)
                if (search_results):
                    cont = False
                if remaining < 10:
                    print("|",end="")
                    sonno = reset-int(time.time())+10
                    print(sonno)
                    time.sleep(sonno)
            
            
            except Exception, err:
                print (traceback.format_exc())
                print("|",end="")
                time.sleep(910)
                continue
        
        statuses = search_results['statuses']
        print(":",end="")
        for _ in range(15): 
             cont = True
             try:
                 next_results = search_results['search_metadata']['next_results']
             except KeyError: # No more results when next_results doesn't exist
                 break
             # Create a dictionary from next_results, which has the following form:
             # ?max_id=313519052523986943&q=NCAA&include_entities=1
             kwargs = dict([ kv.split('=') for kv in next_results[1:].split("&") ])
             
             
             while (cont):
                 try:
                     search_results = twitter_api.search.tweets(**kwargs)
                     remaining = search_results.rate_limit_remaining                     
                     print(remaining)
                     if (search_results):
                         cont = False
                     if remaining < 10:
                        print("|",end="")
                        sonno = reset-int(time.time())+10
                        print(sonno)
                        time.sleep(sonno)
                 except Exception, err:
                     print (traceback.format_exc())
                     print("|",end="")
                     time.sleep(910)
                     continue
             
             statuses += search_results['statuses']
             print(".",end="")
        
        if (len(statuses)>0):
            #salva su file con nome query
            print("_",end="")
            pickle.dump(statuses,open(join(DATA, q.replace(" ","") +".txt"),"wb"))
            


#==============================================================================
# retrieve info about an user
#==============================================================================
            
def get_users(u,options=None):
        cont = True   
        while(cont):
            try:     
                print(u)
                search_results = twitter_api.users.lookup(screen_name=u) 
                reset = search_results.rate_limit_reset
                remaining = search_results.rate_limit_remaining
                print(reset)
                print(remaining)
                if (search_results):
                    cont = False
                if remaining < 10:
                    print("|",end="")
                    sonno = reset-int(time.time())+10
                    print(sonno)
                    time.sleep(sonno)
            
            
            except Exception, err:
                print (traceback.format_exc())
                print("|",end="")
                time.sleep(910)
                continue
        
        if (len(search_results)>0):
            #salva su file con nome query
            print(search_results[0])
            print("_",end="")
            return search_results


#==============================================================================
#  retrieve timeline for a specific user 
#==============================================================================

def get_timeline(u,diff):
        cont = True   
        while(cont):
            try:     
                print(u)
                search_results = twitter_api.statuses.user_timeline(screen_name = u, since_id=diff[u]['start'], max_id=diff[u]['end']) 
                reset = search_results.rate_limit_reset
                remaining = search_results.rate_limit_remaining
                print(reset)
                print(remaining)
                print(len(search_results))
                if (search_results):
                    cont = False
                if remaining < 10:
                    print("|",end="")
                    sonno = reset-int(time.time())+10
                    print(sonno)
                    time.sleep(sonno)
            
            
            except Exception, err:
                print (traceback.format_exc())
                print("|",end="")
                time.sleep(910)
                continue
        
        if (len(search_results)>0):
            #salva su file con nome query
            print(search_results[0])
            print("_",end="")
            return search_results