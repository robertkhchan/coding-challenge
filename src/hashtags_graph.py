'''
Created on Mar 30, 2016

@author: robert
'''
import copy

class HashtagsGraph(object):
    '''
    classdocs
    '''
    
    def __init__(self):
        self.processed_entries = dict() # {datetime: [{str}]}
        self.hashtags_graph = dict()    # {str: {str}}
        pass
    
    
    def update(self, entry):
        '''
        Arguments:
            entry (tuple): takes the form (datetime, {str})
        '''
        current_list = self.processed_entries.get(entry[0],[])
        current_list += [entry[1]]
        self.processed_entries[entry[0]] = current_list
        
        if (len(entry[1]) > 1):
            for hashtag in entry[1]:
                related_tags = copy.deepcopy(entry[1]).remove(hashtag)
                self.update_graph(hashtag, related_tags)

    
    def update_graph(self, hashtag, related_tags):
        '''
        Arguments:
            hashtag (str)
            related_tags ({str})
        '''
        existing_related_tags = self.hashtags_graph.get(hashtag, set())
        existing_related_tags |= related_tags
        self.hashtags_graph[hashtag] = existing_related_tags

