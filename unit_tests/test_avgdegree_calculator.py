'''
Created on Mar 30, 2016

@author: robert
'''
import unittest
from src.avgdegree_calculator import AverageDegreeCalculator


class TestAverageDegreeCalculator(unittest.TestCase):


    def test_calculate_single_edge(self):
        
        edge_counts = {
            ("apache","spark"):1
        }
        
        avg_deg = AverageDegreeCalculator().calculate(edge_counts)
        
        self.assertEquals("1.00", avg_deg)

        
    def test_calculate_multi_edges(self):
        
        edge_counts = {
            ("apache","spark"):1,
            ("apache","storm"):1,
            ("apache","hadoop"):1,
            ("hadoop","storm"):1,
        }
        
        avg_deg = AverageDegreeCalculator().calculate(edge_counts)
        
        self.assertEquals("2.00", avg_deg)

        
    def test_calculate_truncate(self):
        
        edge_counts = {
            ("flink","spark"):1,
            ("hbase","spark"):1,
            ("apache","storm"):1,
            ("apache","hadoop"):1,
            ("storm","hadoop"):1,
        }
        
        avg_deg = AverageDegreeCalculator().calculate(edge_counts)
        
        self.assertEquals("1.66", avg_deg)
