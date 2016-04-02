'''
Created on Mar 30, 2016

@author: Robert Chan
'''
from datetime import datetime
import json

class TweetParser(object):
    '''
    Helper class to parse single tweet entry into a tuple of datetime and hashtags set
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
        
        # Only tweets contain "created_at" attribute is considered of interest
        if ("created_at" in data.keys()):
            created_at = datetime.strptime(data["created_at"], "%a %b %d %H:%M:%S +0000 %Y")
            
            hashtags = set()
            for hashtag in data["entities"]["hashtags"]:
                hashtags.add(hashtag["text"])
                
            return (created_at, hashtags)
        
        # Otherwise, return None
        else:
            return None
        