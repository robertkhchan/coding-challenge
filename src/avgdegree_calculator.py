'''
Created on Mar 30, 2016

@author: robert
'''

class AverageDegreeCalculator(object):
    '''
    classdocs
    '''
    
    def calculate(self, hashtags_edge_count):
        '''
        Arguments: 
            hashtags_graph (dict): takes the form {hashtag : {related_tags}, hashtag: {related_tags}}
            
        Return:
            avg_deg (float) with two significant places
        '''
        avg_deg = 0.0
        
        if (len(hashtags_edge_count) > 0):
            all_edges = hashtags_edge_count.keys()
            all_nodes = {element for pair in all_edges for element in pair}
            avg_deg = (len(all_edges) * 2)/len(all_nodes)
            
        return ("%.3f" % avg_deg)[:-1]
        
    