# -*- coding: utf-8 -*-
"""
Created on Thu Jul  2 13:13:40 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""

import System
import Component
import RSGroup
import numpy as np
import Priorities
import unittest

# Add more checks as you notice issues
class TestPriorities(unittest.TestCase):
    
    def setUp(self):    
        # five component example community from the iReCoDeS paper
        self.five_comp_sys = [dict(), dict(), dict()]
        self.five_comp_sys[0] = {'LocalityID': 1,
                                'Coord. X': 5,
                                'Coord. Y': 5,
                                'Content': {'EPP': 1,
                                            'BTS': 1}} 
        
        self.five_comp_sys[1] = {'LocalityID': 2,
                                'Coord. X': 0,
                                'Coord. Y': 0,
                                'Content': {'CWF': 1}}
        
        self.five_comp_sys[2] = {'LocalityID': 3,
                                'Coord. X': 10,
                                'Coord. Y': 0,
                                'Content': {'BTS': 1,
                                            'BSU': 1}}
        
        self.considered_utilities = ['ElectricPower', 'HighLevelCommunication',
                                     'LowLevelCommunication', 'PotableWater', 
                                     'CoolingWater']
        self.considered_transfer_services = ['PowerLine', 'Pipe']
        self.sys_test = System.System(self.considered_utilities, 
                                 self.considered_transfer_services)
        self.sys_test.create_system(self.five_comp_sys)
        self.priorities = Priorities.PrioritiesFiveCompSys()
        
    def test_get_component_ids(self):
        self.priorities.get_component_ids(self.sys_test)
        self.assertEqual(self.priorities.IDs['EPP'], 1)
        self.assertEqual(self.priorities.IDs['BSU'], 6)
        self.assertEqual(self.priorities.IDs['CWF'], 5)
        
        self.assertEqual(self.priorities.IDs['BTS'], 3)
        
        
    def test_set_all_priorities(self):
        self.priorities.set_all_priorities(self.sys_test)
        self.assertTrue(np.all(self.priorities.utilities['ElectricPower'] == np.asarray([1, 3, 5, 6])))
        self.assertTrue(np.all(self.priorities.utilities['CoolingWater'] == np.asarray([5, 1, 3, 6])))
        self.assertTrue(np.all(self.priorities.utilities['LowLevelCommunication'] == np.asarray([3, 1, 5, 6])))
        
    def test_get_sort_vector(self):
        self.priorities.set_all_priorities(self.sys_test)
        sort_vector = self.priorities.get_sort_vector(self.sys_test, 'ElectricPower')
        self.assertTrue(np.all(sort_vector == [0, 1, 3, 2, 4]))
        sort_vector = self.priorities.get_sort_vector(self.sys_test, 'CoolingWater')
        self.assertTrue(np.all(sort_vector == [2, 0, 1, 3, 4]))
        sort_vector = self.priorities.get_sort_vector(self.sys_test, 'LowLevelCommunication')
        self.assertTrue(np.all(sort_vector == [1, 3, 0, 2, 4]))
        

            
if __name__ == '__main__':
    unittest.main()  