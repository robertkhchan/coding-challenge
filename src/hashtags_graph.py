'''
Created on Mar 30, 2016

@author: robert
'''
#import copy
from datetime import timedelta
from itertools import combinations

class HashtagsGraph(object):
    '''
    classdocs
    '''
    
    def __init__(self, sliding_window_seconds=60):
        self.processed_entries = dict() # {datetime: [{str}]}
        self.hashtags_edge_count = dict() # {(str,str): int}
        self.sliding_window_seconds = timedelta(seconds=sliding_window_seconds)

    def earliest_processed_timestamp(self):
        return next(iter(sorted(self.processed_entries.keys())), None)    
    
    def latest_processed_timestamp(self):
        return next(iter(sorted(self.processed_entries.keys(), reverse=True)), None)
    
    def update(self, entry):
        '''
        Arguments:
            entry (tuple): takes the form (datetime, {str})
        '''    
        latest_processed_timestamp = self.latest_processed_timestamp()
        if (latest_processed_timestamp is not None 
        and entry[0] < latest_processed_timestamp - self.sliding_window_seconds):
            return
        
        earliest_processed_timestamp = self.earliest_processed_timestamp()
        if (earliest_processed_timestamp is not None 
        and earliest_processed_timestamp < entry[0] - self.sliding_window_seconds):
            self.purge_before(entry[0] - self.sliding_window_seconds)

        self.insert(entry)
                
    
    def insert(self, entry):
        self.processed_entries[entry[0]] = self.processed_entries.get(entry[0],[]) + [entry[1]]
        
        if (len(entry[1]) > 1):
            self.increment_edge_count(entry[1])


    def purge_before(self, datetime_to_purge):
        entries_to_purge = {key: value for (key, value) in self.processed_entries.items() if key < datetime_to_purge}
        entries_to_key   = {key: value for (key, value) in self.processed_entries.items() if key >= datetime_to_purge}
        self.processed_entries = entries_to_key

        for entries in entries_to_purge.items():
            for entry in entries[1]:
                if (len(entry) > 1):
                    self.decrement_edge_count(entry)
                        
                        
    def increment_edge_count(self, hashtags):
        for hashtags_edge in combinations(sorted(hashtags), 2):
            self.hashtags_edge_count[hashtags_edge] = self.hashtags_edge_count.get(hashtags_edge,0) + 1

            
    def decrement_edge_count(self, hashtags):
        for hashtags_edge in combinations(sorted(hashtags), 2):
            if hashtags_edge in self.hashtags_edge_count:
                if (self.hashtags_edge_count[hashtags_edge] > 1):
                    self.hashtags_edge_count[hashtags_edge] -= 1
                else:
                    self.hashtags_edge_count.pop(hashtags_edge) 
