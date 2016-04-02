'''
Created on Mar 30, 2016

@author: Robert Chan
'''

class AverageDegreeCalculator(object):
    '''
    Helper class to calculate average degree of hashtags graph
    '''
    
    def calculate(self, hashtags_edge_count):
        '''
        Arguments: 
            hashtags_edge_count (dict): takes the form {(str,str): int}
            
        Return:
            avg_deg (float) truncated to two digits after the decimal place
        '''
        avg_deg = 0.0
        
        if (len(hashtags_edge_count) > 0):
            all_edges = hashtags_edge_count.keys()
            all_nodes = {element for pair in all_edges for element in pair}
            avg_deg = (len(all_edges) * 2)/len(all_nodes)
            
        return ("%.3f" % avg_deg)[:-1]
        
    