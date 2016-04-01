'''
Created on Mar 31, 2016

@author: robert
'''
import unittest
from src.hashtags_graph import HashtagsGraph
from datetime import datetime


class TestHashtagsGraph(unittest.TestCase):
            
        
    def testInsert(self):
        graph = HashtagsGraph()
        
        self.assertEquals(0, len(graph.processed_entries))
        self.assertEquals(0, len(graph.hashtags_edge_count))
        
        # insert entry with single hashtag; will not be inserted
        created_at_0 = datetime(2016, 3, 31, 3, 28, 12)
        hashtags_0 = {"spark"}
        entry_0 = (created_at_0, hashtags_0)
        
        graph.insert(entry_0)
        
        self.assertEquals(1, len(graph.processed_entries))
        self.assertEquals([hashtags_0], graph.processed_entries[created_at_0])
        self.assertEquals(0, len(graph.hashtags_edge_count))
        
        # insert entry with two hashtags; insert as expected
        created_at_1 = datetime(2016, 3, 31, 3, 28, 13)
        hashtags_1 = {"spark", "hadoop"}
        entry_1 = (created_at_1, hashtags_1)
        
        graph.insert(entry_1)
        
        self.assertEquals(2, len(graph.processed_entries))
        self.assertEquals([hashtags_1], graph.processed_entries[created_at_1])
        
        self.assertEquals(1, len(graph.hashtags_edge_count))
        self.assertEquals(1, graph.hashtags_edge_count[("hadoop","spark")])
        
        # insert entry with duplicate hashtags; graph increase by differences
        created_at_2 = datetime(2016, 3, 31, 3, 28, 14)
        hashtags_2 = {"spark", "hadoop", "apache"}
        entry_2 = (created_at_2, hashtags_2)
        graph.insert(entry_2)
        
        self.assertEquals(3, len(graph.processed_entries))
        self.assertEquals([hashtags_2], graph.processed_entries[created_at_2])
        
        self.assertEquals(3, len(graph.hashtags_edge_count))
        self.assertEquals(2, graph.hashtags_edge_count[("hadoop","spark")])
        self.assertEquals(1, graph.hashtags_edge_count[("apache","hadoop")])
        self.assertEquals(1, graph.hashtags_edge_count[("apache","spark")])
    
        # insert entry with completely different hashtags; insert as expected
        created_at_3 = datetime(2016, 3, 31, 3, 28, 15)
        hashtags_3 = {"hello", "world"}
        entry_3 = (created_at_3, hashtags_3)
        graph.insert(entry_3)
        
        self.assertEquals(4, len(graph.processed_entries))
        self.assertEquals([hashtags_3], graph.processed_entries[created_at_3])
        
        self.assertEquals(4, len(graph.hashtags_edge_count))
        self.assertEquals(2, graph.hashtags_edge_count[("hadoop","spark")])
        self.assertEquals(1, graph.hashtags_edge_count[("apache","hadoop")])
        self.assertEquals(1, graph.hashtags_edge_count[("apache","spark")])
        self.assertEquals(1, graph.hashtags_edge_count[("hello","world")])
        
        # insert entry with same timestamp
        created_at_4 = datetime(2016, 3, 31, 3, 28, 15)
        hashtags_4 = {"spark", "pig"}
        entry_4 = (created_at_4, hashtags_4)
        graph.insert(entry_4)
        
        self.assertEquals(4, len(graph.processed_entries))
        self.assertEquals([hashtags_3, hashtags_4], graph.processed_entries[created_at_4])
        
        self.assertEquals(5, len(graph.hashtags_edge_count))
        self.assertEquals(2, graph.hashtags_edge_count[("hadoop","spark")])
        self.assertEquals(1, graph.hashtags_edge_count[("apache","hadoop")])
        self.assertEquals(1, graph.hashtags_edge_count[("apache","spark")])
        self.assertEquals(1, graph.hashtags_edge_count[("hello","world")])
        self.assertEquals(1, graph.hashtags_edge_count[("pig","spark")])


    def testPurgeBefore(self):
        graph = HashtagsGraph()
        
        created_at_0 = datetime(2016, 3, 31, 3, 28, 12); hashtags_0 = {"spark"}
        created_at_1 = datetime(2016, 3, 31, 3, 28, 13); hashtags_1 = {"spark", "hadoop"}
        created_at_2 = datetime(2016, 3, 31, 3, 28, 14); hashtags_2 = {"spark", "hadoop", "apache"}
        created_at_3 = datetime(2016, 3, 31, 3, 28, 15); hashtags_3 = {"hello", "world"}; hashtags_4 = {"spark", "pig"}
        graph.processed_entries = {
            created_at_0:[hashtags_0],
            created_at_1:[hashtags_1],
            created_at_2:[hashtags_2],
            created_at_3:[hashtags_3, hashtags_4]
        }
        
        graph.hashtags_edge_count[("hadoop","spark")] = 2
        graph.hashtags_edge_count[("apache","hadoop")] = 1
        graph.hashtags_edge_count[("apache","spark")] = 1
        graph.hashtags_edge_count[("hello","world")] = 1
        graph.hashtags_edge_count[("pig","spark")] = 1
        
        # purge first entry
        graph.purge_before(datetime(2016, 3, 31, 3, 28, 13))
        
        self.assertEquals(3, len(graph.processed_entries))
        self.assertFalse(created_at_0 in graph.processed_entries.keys())
        
        self.assertEquals(5, len(graph.hashtags_edge_count))
        graph.hashtags_edge_count[("hadoop","spark")] = 2
        graph.hashtags_edge_count[("apache","hadoop")] = 1
        graph.hashtags_edge_count[("apache","spark")] = 1
        graph.hashtags_edge_count[("hello","world")] = 1
        graph.hashtags_edge_count[("pig","spark")] = 1
        
        # purge second entry
        graph.purge_before(datetime(2016, 3, 31, 3, 28, 14))
        
        self.assertEquals(2, len(graph.processed_entries))
        self.assertFalse(created_at_0 in graph.processed_entries.keys())
        self.assertFalse(created_at_1 in graph.processed_entries.keys())
        
        self.assertEquals(5, len(graph.hashtags_edge_count))
        graph.hashtags_edge_count[("hadoop","spark")] = 1
        graph.hashtags_edge_count[("apache","hadoop")] = 1
        graph.hashtags_edge_count[("apache","spark")] = 1
        graph.hashtags_edge_count[("hello","world")] = 1
        graph.hashtags_edge_count[("pig","spark")] = 1
        
        # purge third entry
        graph.purge_before(datetime(2016, 3, 31, 3, 28, 15))
        
        self.assertEquals(1, len(graph.processed_entries))
        self.assertFalse(created_at_2 in graph.processed_entries.keys())
        
        self.assertEquals(2, len(graph.hashtags_edge_count))
        graph.hashtags_edge_count[("hello","world")] = 1
        graph.hashtags_edge_count[("pig","spark")] = 1
                
        # purge fourth and fifth entries
        graph.purge_before(datetime(2016, 3, 31, 3, 28, 16))
        
        self.assertEquals(0, len(graph.processed_entries))
        self.assertEquals(0, len(graph.hashtags_edge_count))

