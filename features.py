# -*- coding: utf-8 -*-
from __future__ import division, print_function
from collections import Counter
import nltk
import math
import time
import re

"""
Created on Mon May 27 01:19:15 2013

@author: Seby
"""

#==============================================================================
#  Features
#==============================================================================

def to_epoch(s):
    return time.mktime(time.strptime(s,'%a %b %d %H:%M:%S +0000 %Y'))

def to_rt_score(retweet,followers):
    if retweet == 0:
        return 0
    if followers == 0:
        followers = 1       
    expected_value = math.pow(5.5,math.log(followers,10)-2.5)
    return retweet/expected_value

def time_feat(value,name):
    features = {}
    features[name+'<30Days'] = (value>1367016168)  
    features['1Month<=' + name +'<6Months' ] = (value>=1353969768 and value<=1367016168)
    features['6Months<=' + name +'<1Year'] = (value>=1338072168 and value<=1353969768)
    features[name+'>1Year'] = (value<1338072168)  
    return features

def n_feat(value,name,M=5):
    features = {}
    features[name+'<'+str(M/5*1)] = (value<(M/5*1))  
    features[str(M/5*1) + '<=' + name +'<' +str( M/5*3)] = (value>=(M/5*1) and value<(M/5*3))
    features[str(M/5*3) + '<=' + name +'<' +str(M)] = (value>=(M/5*3) and value<M)
    features[name+'>='+str(M)] = (value>=M)  
    return features

def n_feat2(value,name,solitari):
    features = {}
    if (solitari):
        features[name+'==0'] = (value==0)  
    features[name+'==1'] = (value==1)  
    features['1<' + name +'<=2.5'] = (value>1 and value<=2.5)
    features['2.5<' + name +'<=5  '] = (value>2.5 and value<=5)
    features['5<' + name +' <=7.5'] = (value>5 and value<=7.5)
    features['7.5<' + name +'< 10 '] = (value>7.5 and value<10)    
    features[name+'== 10'] = (value==10)  
    return features

def log_feat(value,name,M=7):
    features = {}
    value = math.log((value+1),10)
    features = {}
    features[name+'<'+str(M/7*1)] = (value<(M/7*1))  
    features[str(M/7*1) + '<=' + name +'<' +str( M/7*3)] = (value>=(M/7*1) and value<=(M/7*3))
    features[str(M/7*3) + '<=' + name +'<' +str(M/7*5)] = (value>=(M/7*3) and value<=(M/7*5))
    features[str(M/7*5) + '<=' + name +'<' +str(M)] = (value>=(M/7*5) and value<=M)
    features[name+'>'+str(M)] = (value>=M)  
    return features

def avg_w_l_feats(text):
    '''Produces value features "avg<>n: <true|false>" '''
    features = {}
    avg = sum([len(w) for w in text.split()])/len(text.split())
    features['avg<3'] = (avg<3)  
    features['3<=avg<5'] = (avg>=3 and avg<5)
    features['5<=avg<7'] = (avg>=5 and avg<7)    
    features['avg>=7'] = (avg>=7)  
    return features

def lex_d_feats(document):
    '''Produces value features "lex<>n: <true|false>" '''
    features = {}
    lex = len(set(document.split()))/len(document.split())
    features['lex<2'] = (lex<2)  
    features['2<=lex<=4'] = (lex>=2 and lex<=4)
    features['lex>4'] = (lex>4)  
    features = {}
    return features

def has_feats(document, features_words):
    '''Produces binary features "has('word'): <true|false>" '''
    features = {}
    document = set(nltk.word_tokenize(document.lower()))
    for word in features_words:
        features['has_word({})'.format(word[0])] = (word[0] in document)
    return features
    
def has_url(urls, top_urls):
    '''Produces binary features "has('word'): <true|false>" '''
    features = {}  

    nuovi_url = []

    for t in urls:
        matchObj = re.search( r'//(.*?)/', t['expanded_url'], re.I)
        if matchObj != None:                
            actual_url = (matchObj.group(1))
            nuovi_url.append(actual_url)
    
    for f in top_urls:
            features['has_url({})'.format(f[0])] = (f[0] in nuovi_url)
                
    return features
    
def has_hash(hashs, top_hash):
    '''Produces binary features "has('word'): <true|false>" '''
    features = {}
    nuovi_hash = []    
    
    for t in hashs:
        nuovi_hash.append(t['text'].lower())
    
    for f in top_hash:
            features['has_hash({})'.format(f[0])] = (f[0] in nuovi_hash)
           
    return features

def has_names(hashs, top_hash):
    '''Produces binary features "has('word'): <true|false>" '''
    features = {}
    nuovi_hash = []    
    
    for t in hashs:
        nuovi_hash.append(t['screen_name'].lower() )
    
    for f in top_hash:
            features['has_name({})'.format(f[0])] = (f[0] in nuovi_hash)
           
    return features

#==============================================================================
#  GET FEATURES    
#==============================================================================
    
def get_features(tweet,opt):
    retweeted = tweet.has_key('retweeted_status') and tweet['retweet_count']>0   
    if retweeted:
        user = opt[4][tweet['user_ret']]
    else:
        user = opt[4][tweet['user']]
        
    features={}
#==============================================================================
#   Time Related                
#==============================================================================
    if 4 in opt[5]:       
        features.update(n_feat2(tweet['posizione_serie'],"s.pos.",True))
        features.update(n_feat(tweet['lunghezza_serie'],"s.length",1500))
    
    if 5 in opt[5]:       
    
        features.update(n_feat2(tweet['posizione_serie'],"s.pos.",False))
        features.update(n_feat(tweet['lunghezza_serie'],"s.length",1500))
#==============================================================================
#   Text Related
#==============================================================================
    if 1 in opt[5]:       
    
        features.update(has_feats(tweet['text'],opt[0]))
        
        features.update(has_hash(tweet['entities']['hashtags'],opt[1]))
        
        features.update(has_names(tweet['entities']['user_mentions'],opt[2]))

        features.update(avg_w_l_feats(tweet['text']))
        features.update(lex_d_feats(tweet['text']))
        
#==============================================================================
#   Tweet Related
#==============================================================================
    if 2 in opt[5]:       
     
        features.update(n_feat(len(tweet['entities']['hashtags']),"hashtags"))          
        features.update(n_feat(len(tweet['entities']['urls']),"urls"))   
        features.update(has_url(tweet['entities']['urls'],opt[3]))
        
    ###features.update(n_feat(len(tweet['entities']['media']),"hashtags"))      
    
    
#==============================================================================
#    User Related 
#==============================================================================
    if 3 in opt[5]:    
        
        features['verified']=user['verified']
        features['has_default_profile'] = user['default_profile']
        features['has_default_avatar'] = user['default_profile_image']
        features.update(log_feat(user['followers_count'],"log(follow_count)"))
        features.update(log_feat(user['friends_count'],"log(friends_count)"))
        features.update(log_feat(user['statuses_count'],"log(statuses_count)"))
        features.update(time_feat(user['created_at'],"user"))
    
    
    
    return (features,tweet['punteggio']>1)
    #return (features,retweeted)
#==============================================================================
#  Evaluate a classifier in terms of Accuracy, Precision, Recall, F-Measure
#==============================================================================

def evaluate(classifier, test_set):

    def f_measure(precision,recall,alpha):
        try:
            return 1/(alpha*(1/precision)+(1-alpha)*1/recall)
        except ZeroDivisionError:
            print("Division by 0")
            return 1

    test = classifier.batch_classify([fs for (fs,l) in test_set])
    gold = [l for (fs,l) in  test_set]
    matrix = nltk.ConfusionMatrix(gold, test)
    print("")
    
    print(matrix)
    tp = (matrix[True,True])
    fn = (matrix[True,False])
    fp = (matrix[False,True])

    accuracy = nltk.classify.accuracy(classifier, test_set)

    precision = tp/(tp+fp)
    recall = tp/(tp+fn)
    f = f_measure(precision, recall, 0.5)
    print ("F-measure: {:.2f} - Accuracy: {:.2f} - Precision: {:.2f} - "
    "Recall: {:.2f}".format(f,accuracy,precision,recall))
    return [round(f,2),round(accuracy,2),round(precision,2),round(recall,2)]

