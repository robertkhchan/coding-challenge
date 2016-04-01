'''
Created on Mar 30, 2016

@author: robert
'''
import unittest
from src.avgdegree_calculator import AverageDegreeCalculator


class TestAverageDegreeCalculator(unittest.TestCase):


    def test_calculate(self):
        
        hashtags_edge_count = {("apache","spark"):1}
        
        calculator = AverageDegreeCalculator()
        
        avg_deg = calculator.calculate(hashtags_edge_count)
        
        self.assertEquals('%.2f' % 1.00, avg_deg)