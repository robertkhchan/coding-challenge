'''
Created on Mar 30, 2016

@author: robert
'''
from datetime import datetime
import json

class TweetParser(object):
    '''
    classdocs
    '''
    
    def parse(self, tweet):
        '''
        Arguments:
            tweet (str): string of Twitter tweet in json format
            
        Return:
            tuple of datetime and set of tags if tweet is of interest, 
            None otherwise
        '''
        
        data = json.loads(tweet, strict=False)
        if ("created_at" in data.keys()):
            created_at = datetime.strptime(data["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
            hashtags = {}
            for entry in data["entities"]["hashtags"]:
                hashtags.append(entry["text"])
                return (created_at, hashtags)
        else:
                return None
        