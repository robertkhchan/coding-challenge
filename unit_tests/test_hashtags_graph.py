'''
Created on Mar 31, 2016

@author: robert
'''
import unittest
from src.hashtags_graph import HashtagsGraph


class TestHashtagsGraph(unittest.TestCase):


    def testUpdateGraph(self):
        graph = HashtagsGraph()
        
        self.assertEquals(0, len(graph.hashtags_graph))
        
        # update new graph with new hashtag entry
        hashtag = "spark"
        related_tags = {"apache"}
        graph.update_graph(hashtag, related_tags)
        
        self.assertEquals(1, len(graph.hashtags_graph))
        self.assertEquals({"apache"}, graph.hashtags_graph["spark"])

        # update graph with existing hashtag        
        related_tags = {"hadoop"}

        graph.update_graph(hashtag, related_tags)
        
        self.assertEquals(1, len(graph.hashtags_graph))
        self.assertEquals({"apache", "hadoop"}, graph.hashtags_graph["spark"])
                
        # update graph with existing related_tag
        related_tags = {"apache", "pig"}

        graph.update_graph(hashtag, related_tags)
        
        self.assertEquals(1, len(graph.hashtags_graph))
        self.assertEquals({"apache", "hadoop", "pig"}, graph.hashtags_graph["spark"])
        