# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 13:07:58 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""

import unittest
import RSGroup
import collections

# Add more checks as you notice issues
class TestRSGroup(unittest.TestCase):
    
    def setUp(self):
        self.rs_list_1 = RSGroup.OrderedDefaultDict([('rs1', 5),
                                                  ('rs2', 4),
                                                  ('rs3', 3)])
        
        self.rsgroup_1 = RSGroup.RSGroup()
        
    def test_constructor(self):              
        # test if default values (for non-existant keys) are zero
        self.assertEqual(self.rsgroup_1.initial['a'], 0)
    
    def test_initial_values(self):              
        self.rsgroup_1.set_initial_rs_value(self.rs_list_1)      
        # test if the attributes exist and are named correctly   
        self.assertEqual(self.rsgroup_1.initial['rs1'], 5)
        self.assertEqual(self.rsgroup_1.initial['rs2'], 4)
        self.assertEqual(self.rsgroup_1.initial['rs3'], 3)
        # check if non existant key returns 0
        self.assertEqual(self.rsgroup_1.initial['rs4'], 0)                      
      
    def test_get_rs_vector(self):       
        self.rsgroup_1.set_initial_rs_value(self.rs_list_1)
        rs_vector = self.rsgroup_1.get_rs_vector(self.rs_list_1.keys())
        self.assertEqual(rs_vector, [5, 4, 3])
        
    def test_update(self):        
        self.rsgroup_1.set_initial_rs_value(self.rs_list_1)
        func_level = 0.3
        self.rsgroup_1.update(func_level)
        self.assertEqual(self.rsgroup_1.current['rs1'], 5*func_level)
        self.assertEqual(self.rsgroup_1.current['rs2'], 4*func_level)
        self.assertEqual(self.rsgroup_1.current['rs3'], 3*func_level)        
        self.assertEqual(self.rsgroup_1.initial['rs1'], 5)
        self.assertEqual(self.rsgroup_1.initial['rs2'], 4)
        self.assertEqual(self.rsgroup_1.initial['rs3'], 3)
        
            
        
if __name__ == '__main__':
    unittest.main()       

