'''
Created on Mar 30, 2016

@author: Robert Chan
'''
from datetime import timedelta
from itertools import combinations

class HashtagsGraph(object):
    '''
    Hashtags graph that stores: 
        - a list of tweet entries in the past sliding_window_seconds
        - a dictionary of edges and their counts
    '''
    
    def __init__(self, sliding_window_seconds=60):
        self.sliding_window_seconds = timedelta(seconds=sliding_window_seconds)
        self.processed_entries = dict() # {datetime: [{str}]}
        self.edge_counts = dict() # {(str,str): int}

    
    def update(self, entry):
        '''Update hashtags graph with a valid tweet entry tuple that takes the form (datetime, {str})
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


    def earliest_processed_timestamp(self):
        '''Return the timestamp of the earliest tweet entry being processed
        '''
        return next(iter(sorted(self.processed_entries.keys())), None)    
    
    
    def latest_processed_timestamp(self):
        '''Return the timestamp of the latest tweet entry being processed
        '''
        return next(iter(sorted(self.processed_entries.keys(), reverse=True)), None)                
    
    
    def insert(self, entry):
        '''Insert an entry to the list of currently processed entries 
           and update hashtags graph if necessary
        '''
        self.processed_entries[entry[0]] = self.processed_entries.get(entry[0],[]) + [entry[1]]
        
        if (len(entry[1]) > 1):
            self.increment_edge_count(entry[1])
                        
                        
    def increment_edge_count(self, hashtags):
        '''Increatement edge count for every pair of tag in hashtags
        '''
        for hashtags_edge in combinations(sorted(hashtags), 2):
            self.edge_counts[hashtags_edge] = self.edge_counts.get(hashtags_edge,0) + 1


    def purge_before(self, datetime_to_purge):
        '''Purge any entries before datetime_to_purge from the list of currently processed entries
           and update hashtags graph if necessary 
        '''
        entries_to_purge = {key: value for (key, value) in self.processed_entries.items() if key < datetime_to_purge}
        entries_to_keep   = {key: value for (key, value) in self.processed_entries.items() if key >= datetime_to_purge}
        self.processed_entries = entries_to_keep

        for entries in entries_to_purge.items():
            for entry in entries[1]:
                if (len(entry) > 1):
                    self.decrement_edge_count(entry)
                        
            
    def decrement_edge_count(self, hashtags):
        '''Decrement edge count for every pair of tag in hashtags
        '''
        for hashtags_edge in combinations(sorted(hashtags), 2):
            if hashtags_edge in self.edge_counts:
                if (self.edge_counts[hashtags_edge] > 1):
                    self.edge_counts[hashtags_edge] -= 1
                else:
                    self.edge_counts.pop(hashtags_edge) 
