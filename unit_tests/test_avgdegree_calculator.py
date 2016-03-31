'''
Created on Mar 30, 2016

@author: robert
'''
import unittest
from src.avgdegree_calculator import AverageDegreeCalculator


class TestAverageDegreeCalculator(unittest.TestCase):


    def test_calculate(self):
        hashtags_graph = {"spark": {"apahce"}, "apache":{"spark"}}
        calculator = AverageDegreeCalculator()
        
        avg_deg = calculator.calculate(hashtags_graph)
        
        self.assertEquals(1.0, avg_deg)