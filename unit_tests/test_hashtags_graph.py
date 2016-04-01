'''
Created on Mar 31, 2016

@author: robert
'''
import unittest
from src.hashtags_graph import HashtagsGraph
from datetime import datetime


class TestHashtagsGraph(unittest.TestCase):
            
        
    def testUpdateAndLatestProcessedTimestamp(self):
        graph = HashtagsGraph()
        
        # Assert on empty graph
        self.assertTrue(graph.latest_processed_timestamp() is None)
        
        # Assert latest timestamp on very first entry
        created_at_1 = datetime(2016, 3, 31, 3, 28, 13)
        hashtags_1 = {"spark", "hadoop"}
        entry_1 = (created_at_1, hashtags_1)
        graph.update(entry_1)
        
        self.assertEquals(1, len(graph.processed_entries))
        self.assertEquals([hashtags_1], graph.processed_entries[created_at_1])
        self.assertEquals(created_at_1, graph.latest_processed_timestamp())
        
        # Assert latest timestamp on entry older than first entry by more than a minute
        created_at_2 = datetime(2016, 2, 27, 3, 28, 13)
        hashtags_2 = {"apache", "hadoop"}
        entry_2 = (created_at_2, hashtags_2)
        graph.update(entry_2)
        
        self.assertEquals(1, len(graph.processed_entries))
        self.assertEquals([hashtags_1], graph.processed_entries[created_at_1])
        self.assertEquals(created_at_1, graph.latest_processed_timestamp())
        
        # Assert latest timestamp on entry newer than first entry
        created_at_3 = datetime(2016, 3, 31, 3, 29, 0)
        hashtags_3 = {"apache", "hadoop"}
        entry_3 = (created_at_3, hashtags_3)
        graph.update(entry_3)
        
        self.assertEquals(2, len(graph.processed_entries))
        self.assertEquals([hashtags_3], graph.processed_entries[created_at_3])
        self.assertEquals(created_at_3, graph.latest_processed_timestamp())
        
        
    def testInsert(self):
        graph = HashtagsGraph()
        
        self.assertEquals(0, len(graph.hashtags_graph))
        
        # insert entry with single hashtag; will not be inserted
        created_at_0 = datetime(2016, 3, 31, 3, 28, 12)
        hashtags_0 = {"spark"}
        entry_0 = (created_at_0, hashtags_0)
        graph.insert(entry_0)
        
        self.assertEquals(1, len(graph.processed_entries))
        self.assertEquals([hashtags_0], graph.processed_entries[created_at_0])
        self.assertEquals(0, len(graph.hashtags_graph))
        
        # insert entry with two hashtags; insert as expected
        created_at_1 = datetime(2016, 3, 31, 3, 28, 13)
        hashtags_1 = {"spark", "hadoop"}
        entry_1 = (created_at_1, hashtags_1)
        graph.insert(entry_1)
        
        self.assertEquals(2, len(graph.processed_entries))
        self.assertEquals([hashtags_1], graph.processed_entries[created_at_1])
        
        self.assertEquals(2, len(graph.hashtags_graph))
        self.assertEquals({"hadoop"}, graph.hashtags_graph["spark"])
        self.assertEquals({"spark"}, graph.hashtags_graph["hadoop"])
        
        # insert entry with duplicate hashtags; graph increase by differences
        created_at_2 = datetime(2016, 3, 31, 3, 28, 14)
        hashtags_2 = {"spark", "hadoop", "apache"}
        entry_2 = (created_at_2, hashtags_2)
        graph.insert(entry_2)
        
        self.assertEquals(3, len(graph.processed_entries))
        self.assertEquals([hashtags_2], graph.processed_entries[created_at_2])
        
        self.assertEquals(3, len(graph.hashtags_graph))
        self.assertEquals({"hadoop", "apache"}, graph.hashtags_graph["spark"])
        self.assertEquals({"spark", "apache"}, graph.hashtags_graph["hadoop"])
        self.assertEquals({"hadoop", "spark"}, graph.hashtags_graph["apache"])
    
        # insert entry with completely different hashtags; insert as expected
        created_at_3 = datetime(2016, 3, 31, 3, 28, 15)
        hashtags_3 = {"hello", "world"}
        entry_3 = (created_at_3, hashtags_3)
        graph.insert(entry_3)
        
        self.assertEquals(4, len(graph.processed_entries))
        self.assertEquals([hashtags_3], graph.processed_entries[created_at_3])
                
        self.assertEquals(5, len(graph.hashtags_graph))
        self.assertEquals({"hadoop", "apache"}, graph.hashtags_graph["spark"])
        self.assertEquals({"spark", "apache"}, graph.hashtags_graph["hadoop"])
        self.assertEquals({"hadoop", "spark"}, graph.hashtags_graph["apache"])
        self.assertEquals({"world"}, graph.hashtags_graph["hello"])
        self.assertEquals({"hello"}, graph.hashtags_graph["world"])
        
        # insert entry with same timestamp
        created_at_4 = datetime(2016, 3, 31, 3, 28, 15)
        hashtags_4 = {"spark", "pig"}
        entry_4 = (created_at_4, hashtags_4)
        graph.insert(entry_4)
        
        self.assertEquals(4, len(graph.processed_entries))
        self.assertEquals([hashtags_3, hashtags_4], graph.processed_entries[created_at_4])
                
        self.assertEquals(6, len(graph.hashtags_graph))
        self.assertEquals({"hadoop", "apache", "pig"}, graph.hashtags_graph["spark"])
        self.assertEquals({"spark", "apache"}, graph.hashtags_graph["hadoop"])
        self.assertEquals({"hadoop", "spark"}, graph.hashtags_graph["apache"])
        self.assertEquals({"world"}, graph.hashtags_graph["hello"])
        self.assertEquals({"hello"}, graph.hashtags_graph["world"])
        self.assertEquals({"spark"}, graph.hashtags_graph["pig"])


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
        
        graph.hashtags_graph["spark"] = {"apache", "hadoop", "pig"}
        graph.hashtags_graph["hadoop"] = {"apache", "spark"}
        graph.hashtags_graph["apache"] = {"spark", "hadoop"}
        graph.hashtags_graph["hello"] = {"world"}
        graph.hashtags_graph["world"] = {"hello"}
        graph.hashtags_graph["pig"] = {"spark"}
        
        self.assertEquals(4, len(graph.processed_entries))
        self.assertEquals([hashtags_0], graph.processed_entries[created_at_0])
        
        self.assertEquals(6, len(graph.hashtags_graph))
        self.assertEquals({"hadoop", "apache", "pig"}, graph.hashtags_graph["spark"])
        self.assertEquals({"spark", "apache"}, graph.hashtags_graph["hadoop"])
        self.assertEquals({"hadoop", "spark"}, graph.hashtags_graph["apache"])
        self.assertEquals({"world"}, graph.hashtags_graph["hello"])
        self.assertEquals({"hello"}, graph.hashtags_graph["world"])
        self.assertEquals({"spark"}, graph.hashtags_graph["pig"])
        
        # purge first entry
        datetime_to_purge = datetime(2016, 3, 31, 3, 28, 14)
        graph.purge_before(datetime_to_purge)
        
        self.assertEquals(2, len(graph.processed_entries))
        self.assertFalse(created_at_0 in graph.processed_entries.keys())
        self.assertFalse(created_at_1 in graph.processed_entries.keys())
        
        self.assertEquals(6, len(graph.hashtags_graph))
        self.assertEquals({"apache","pig"}, graph.hashtags_graph["spark"])
        self.assertEquals({"apache"}, graph.hashtags_graph["hadoop"])
        self.assertEquals({"hadoop", "spark"}, graph.hashtags_graph["apache"])
        self.assertEquals({"world"}, graph.hashtags_graph["hello"])
        self.assertEquals({"hello"}, graph.hashtags_graph["world"])
        self.assertEquals({"spark"}, graph.hashtags_graph["pig"])
        
        # purge second entry
        datetime_to_purge = datetime(2016, 3, 31, 3, 28, 15)
        graph.purge_before(datetime_to_purge)
        
        self.assertEquals(1, len(graph.processed_entries))
        self.assertFalse(created_at_2 in graph.processed_entries.keys())

        self.assertEquals(4, len(graph.hashtags_graph))
        self.assertEquals({"pig"}, graph.hashtags_graph["spark"])
        self.assertEquals({"world"}, graph.hashtags_graph["hello"])
        self.assertEquals({"hello"}, graph.hashtags_graph["world"])
        self.assertEquals({"spark"}, graph.hashtags_graph["pig"])
                
        # purge third entry
        datetime_to_purge = datetime(2016, 3, 31, 3, 28, 16)
        graph.purge_before(datetime_to_purge)
        
        self.assertEquals(0, len(graph.processed_entries))
        self.assertEquals(0, len(graph.hashtags_graph))


    def testAddToGraph(self):
        graph = HashtagsGraph()
        
        self.assertEquals(0, len(graph.hashtags_graph))
        
        # update new graph with new hashtag entry
        hashtag = "spark"
        related_tags = {"apache"}
        graph.add_to_graph(hashtag, related_tags)
        
        self.assertEquals(1, len(graph.hashtags_graph))
        self.assertEquals({"apache"}, graph.hashtags_graph["spark"])

        # update graph with existing hashtag        
        related_tags = {"hadoop"}

        graph.add_to_graph(hashtag, related_tags)
        
        self.assertEquals(1, len(graph.hashtags_graph))
        self.assertEquals({"apache", "hadoop"}, graph.hashtags_graph["spark"])
                
        # update graph with existing related_tag
        related_tags = {"apache", "pig"}

        graph.add_to_graph(hashtag, related_tags)
        
        self.assertEquals(1, len(graph.hashtags_graph))
        self.assertEquals({"apache", "hadoop", "pig"}, graph.hashtags_graph["spark"])
        
    

    def testRemoveFromGraph(self):
        graph = HashtagsGraph()
        graph.hashtags_graph["spark"] = {"apache", "hadoop", "pig"}
        
        self.assertEquals(1, len(graph.hashtags_graph))
        
        # remove existing related_tag from graph
        hashtag = "spark"
        related_tags = {"apache"}
        graph.remove_from_graph(hashtag, related_tags)
        
        self.assertEquals(1, len(graph.hashtags_graph))
        self.assertEquals({"hadoop", "pig"}, graph.hashtags_graph["spark"])

        # remove non-existing related_tag from graph        
        related_tags = {"apache", "pig"}

        graph.remove_from_graph(hashtag, related_tags)
        
        self.assertEquals(1, len(graph.hashtags_graph))
        self.assertEquals({"hadoop"}, graph.hashtags_graph["spark"])
                
        # remove last related_tag from graph
        related_tags = {"hadoop"}

        graph.remove_from_graph(hashtag, related_tags)
        
        self.assertEquals(0, len(graph.hashtags_graph))
