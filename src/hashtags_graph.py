'''
Created on Mar 30, 2016

@author: robert
'''
import copy
from datetime import timedelta

class HashtagsGraph(object):
    '''
    classdocs
    '''
    
    def __init__(self, sliding_window_seconds=60):
        self.processed_entries = dict() # {datetime: [{str}]}
        self.hashtags_graph = dict()  # {str: {str}}
        self.sliding_window_seconds = timedelta(seconds=sliding_window_seconds)
        pass

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


    def purge_before(self, datetime_to_purge):
        
        entries_to_purge = {key: value for (key, value) in self.processed_entries.items() if key < datetime_to_purge}
        entries_to_keep = {key: value for (key, value) in self.processed_entries.items() if key >= datetime_to_purge}
        self.processed_entries = entries_to_keep
        
        for entries in entries_to_purge.items():
            for entry in entries[1]:
                if (len(entry) > 1):
                    for hashtag in entry:
                        related_tags = copy.deepcopy(entry)
                        related_tags.remove(hashtag)
                        self.remove_from_graph(hashtag, related_tags)
                
    
    def insert(self, entry):
        current_list = self.processed_entries.get(entry[0],[])
        current_list += [entry[1]]
        self.processed_entries[entry[0]] = current_list
        
        if (len(entry[1]) > 1):
            for hashtag in entry[1]:
                related_tags = copy.deepcopy(entry[1])
                related_tags.remove(hashtag)
                self.add_to_graph(hashtag, related_tags)

    
    def add_to_graph(self, hashtag, related_tags):
        '''
        Arguments:
            hashtag (str)
            related_tags ({str})
        '''
        existing_related_tags = self.hashtags_graph.get(hashtag, set())
        existing_related_tags |= related_tags
        self.hashtags_graph[hashtag] = existing_related_tags
        
        
    def remove_from_graph(self, hashtag, related_tags):
        '''
        Arguments:
            hashtag (str)
            related_tags ({str})
        '''
        existing_related_tags = self.hashtags_graph.get(hashtag, None)
        if (existing_related_tags is not None):
            existing_related_tags -= related_tags
            if (len(existing_related_tags) > 0):
                self.hashtags_graph[hashtag] = existing_related_tags
            else:
                self.hashtags_graph.pop(hashtag)

