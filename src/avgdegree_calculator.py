'''
Created on Mar 30, 2016

@author: robert
'''

class AverageDegreeCalculator(object):
    '''
    classdocs
    '''
    
    def calculate(self, hashtags_graph):
        '''
        Arguments: 
            hashtags_graph (dict): takes the form {hashtag : {related_tags}, hashtag: {related_tags}}
            
        Return:
            avg_deg (float) with two significant places
        '''
        avg_deg = 0.0
        
        if (len(hashtags_graph) > 0):
            sum_of_degree = 0
            for _, related_tags in hashtags_graph.items():
                sum_of_degree += len(related_tags)
            
            avg_deg = sum_of_degree / len(hashtags_graph)
            
        return "%.2f" % avg_deg
        
    