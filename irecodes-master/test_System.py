# -*- coding: utf-8 -*-
"""
Created on Mon Jun 29 21:32:04 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
 """

import System
import Component
import numpy as np
import unittest
import Priorities
import math

# Add more checks as you notice issues
class TestSystem(unittest.TestCase):
    
    def setUp(self):
        # define the input file for a two locality - two component system
        # rethink how the input file should be designed
        self.two_comp_sys = [dict(), dict()]
        self.two_comp_sys[0] = {'LocalityID': 1,
                                'Coord. X': 0,
                                'Coord. Y': 0,
                                'Content': {'EPP': 1}} 
        
        self.two_comp_sys[1] = {'LocalityID': 2,
                                'Coord. X': 5,
                                'Coord. Y': 5,
                                'Content': {'BSU': 1}}
        
        # two comp system with links
        self.two_comp_sys_wlinks = [dict(), dict()]
        self.two_comp_sys_wlinks[0] = {'LocalityID': 1,
                                'Coord. X': 0,
                                'Coord. Y': 0,
                                'Content': {'EPP': 1},
                                # link to field determines which link types is connected to which locality_id
                                # here locality 1 is connected to locality 2 with one CWP and one EPTL
                                'LinkTo': {'CWP': [2],
                                           'EPTL': [2],
                                           },
                                'BridgeTo': {'CWP': [2],
                                           'EPTL': [2]}}                               
        
        self.two_comp_sys_wlinks[1] = {'LocalityID': 2,
                                'Coord. X': 5,
                                'Coord. Y': 5,
                                'Content': {'BSU': 1},
                                # LinkTo field determines which link types is connected to which locality_id
                                # here locality 1 is connected to locality 2 with one CWP and one EPTL
                                'LinkTo': {'CWP': [1], 'EPTL': [1]},
                                'BridgeTo': {'CWP': [1],
                                           'EPTL': [1],
                                           }}             
        
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
                                'Content': {'PWF': 1,
                                            'BSU': 1}}
        
        self.five_comp_sys_wlinks = [dict(), dict(), dict()]
        self.five_comp_sys_wlinks[0] = {'LocalityID': 1,
                                'Coord. X': 5,
                                'Coord. Y': 5,
                                'Content': {'EPP': 1,
                                            'BTS': 1},
                                'LinkTo': {'CWP': [2, 3],
                                           'EPTL': [2, 3],
                                           'PWP': [2, 3]},
                                'BridgeTo': {'CWP': [2, 3],
                                           'EPTL': [2, 3]}} 
        
        self.five_comp_sys_wlinks[1] = {'LocalityID': 2,
                                'Coord. X': 0,
                                'Coord. Y': 0,
                                'Content': {'CWF': 1},
                                'LinkTo': {'CWP': [1, 3],
                                           'EPTL': [1, 3],
                                           'PWP': [1, 3]},
                                'BridgeTo': {'CWP': [1, 3],
                                           'EPTL': [1, 3]}}
        
        self.five_comp_sys_wlinks[2] = {'LocalityID': 3,
                                'Coord. X': 10,
                                'Coord. Y': 0,
                                'Content': {'PWF': 1,
                                            'BSU': 1},
                                'LinkTo': {'CWP': [2, 1],
                                           'EPTL': [2, 1],
                                           'PWP': [2, 1]},
                                'BridgeTo': {'CWP': [2, 1],
                                             'EPTL': [2, 1]}}
        
        self.considered_utilities = ['ElectricPower', 'HighLevelCommunication',
                                     'LowLevelCommunication', 'PotableWater', 
                                     'CoolingWater']
        self.considered_transfer_services = ['ElectricPowerTransferService', 'CoolingWaterTransferService', 'PotableWaterTransferService']
        self.sys_test = System.System(self.considered_utilities, 
                                 self.considered_transfer_services)
    
    def test_constructor(self):              
        self.assertEqual(self.sys_test.num_utilities, 5)
        self.assertEqual(self.sys_test.num_transfer_services, 3)
        self.assertEqual(self.sys_test.considered_utilities, self.considered_utilities)
        self.assertEqual(self.sys_test.considered_transfer_services, self.considered_transfer_services)
        self.assertEqual(self.sys_test.components, [])
        self.assertEqual(self.sys_test.time_step, 0)
        
    def test_create_system(self):
        # test with two comp system
        self.sys_test.create_system(self.two_comp_sys)
        self.assertTrue(isinstance(self.sys_test.components[0], Component.EPP))
        self.assertTrue(isinstance(self.sys_test.components[1], Component.BSU))
        self.assertTrue(self.sys_test.components[0].start_locality == self.sys_test.components[0].end_locality == 1)        
        self.assertTrue(self.sys_test.components[1].start_locality == self.sys_test.components[1].end_locality == 2)
        # test with two comp system with links
        self.sys_test.create_system(self.two_comp_sys_wlinks)
        self.assertTrue(isinstance(self.sys_test.components[0], Component.EPP))
        self.assertTrue(isinstance(self.sys_test.components[1], Component.Bridge))
        self.assertTrue(isinstance(self.sys_test.components[2], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.components[3], Component.EPTL))
        self.assertTrue(isinstance(self.sys_test.components[4], Component.BSU))
        self.assertTrue(len(self.sys_test.components), 5) 
        self.assertTrue(self.sys_test.components[0].start_locality == self.sys_test.components[0].end_locality == 1)        
        self.assertTrue(self.sys_test.components[1].start_locality == 1 and self.sys_test.components[1].end_locality == 2)
        self.assertTrue(self.sys_test.components[2].start_locality == 1 and self.sys_test.components[2].end_locality == 2)
        self.assertTrue(self.sys_test.components[3].start_locality == 1 and self.sys_test.components[1].end_locality == 2)
        self.assertTrue(self.sys_test.components[4].start_locality == self.sys_test.components[1].end_locality == 2)
        # test with five comp system with links
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        self.assertTrue(len(self.sys_test.components), 17) 
        self.assertTrue(isinstance(self.sys_test.components[0], Component.EPP))
        self.assertTrue(isinstance(self.sys_test.components[1], Component.BTS))
        self.assertTrue(isinstance(self.sys_test.components[2], Component.Bridge))
        self.assertTrue(isinstance(self.sys_test.components[3], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.components[4], Component.Bridge))
        self.assertTrue(isinstance(self.sys_test.components[5], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.components[6], Component.EPTL))
        self.assertTrue(isinstance(self.sys_test.components[7], Component.EPTL))
        self.assertTrue(isinstance(self.sys_test.components[8], Component.PWP))
        self.assertTrue(isinstance(self.sys_test.components[9], Component.PWP))
        self.assertTrue(isinstance(self.sys_test.components[10], Component.CWF))
        self.assertTrue(isinstance(self.sys_test.components[11], Component.Bridge))
        self.assertTrue(isinstance(self.sys_test.components[12], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.components[13], Component.EPTL))
        self.assertTrue(isinstance(self.sys_test.components[14], Component.PWP))
        self.assertTrue(isinstance(self.sys_test.components[15], Component.PWF))
        self.assertTrue(isinstance(self.sys_test.components[16], Component.BSU))
        self.assertTrue(self.sys_test.components[0].start_locality == self.sys_test.components[0].end_locality == 1)
        self.assertTrue(self.sys_test.components[1].start_locality == self.sys_test.components[1].end_locality == 1)        
        self.assertTrue(self.sys_test.components[2].start_locality == 1 and self.sys_test.components[2].end_locality == 2)
        self.assertTrue(self.sys_test.components[3].start_locality == 1 and self.sys_test.components[3].end_locality == 2)
        self.assertTrue(self.sys_test.components[4].start_locality == 1 and self.sys_test.components[4].end_locality == 3)
        self.assertTrue(self.sys_test.components[5].start_locality == 1 and self.sys_test.components[5].end_locality == 3)
        self.assertTrue(self.sys_test.components[6].start_locality == 1 and self.sys_test.components[6].end_locality == 2)
        self.assertTrue(self.sys_test.components[7].start_locality == 1 and self.sys_test.components[7].end_locality == 3)
        self.assertTrue(self.sys_test.components[8].start_locality == 1 and self.sys_test.components[8].end_locality == 2)
        self.assertTrue(self.sys_test.components[9].start_locality == 1 and self.sys_test.components[9].end_locality == 3)
        self.assertTrue(self.sys_test.components[10].start_locality == self.sys_test.components[10].end_locality == 2)
        self.assertTrue(self.sys_test.components[11].start_locality == 2 and self.sys_test.components[11].end_locality == 3)
        self.assertTrue(self.sys_test.components[12].start_locality == 2 and self.sys_test.components[12].end_locality == 3)
        self.assertTrue(self.sys_test.components[13].start_locality == 2 and self.sys_test.components[13].end_locality == 3)
        self.assertTrue(self.sys_test.components[14].start_locality == 2 and self.sys_test.components[14].end_locality == 3)
        self.assertTrue(self.sys_test.components[15].start_locality == self.sys_test.components[15].end_locality == 3)
        self.assertTrue(self.sys_test.components[16].start_locality == self.sys_test.components[16].end_locality == 3)       
       
    def test_set_damage(self):
        damage_vector = [0.4, 0.5]
        self.sys_test.create_system(self.two_comp_sys)
        self.sys_test.set_damage(damage_vector)
        self.assertEqual(self.sys_test.components[0].damage_level, damage_vector[0])
        self.assertEqual(self.sys_test.components[1].damage_level, damage_vector[1])
        
        damage_vector = np.random.rand(17)
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        self.sys_test.set_damage(damage_vector)
        for i, component in enumerate(self.sys_test.components):
            self.assertEqual(component.damage_level, damage_vector[i])
            
            
    def test_repair(self):
        damage_vector = [0.4, 0.5]
        self.sys_test.create_system(self.two_comp_sys)
        self.sys_test.set_damage(damage_vector)
        self.sys_test.repair()
        self.assertEqual(self.sys_test.components[0].damage_level, round(damage_vector[0]-self.sys_test.components[0].repair_rate, 5))
        self.assertEqual(self.sys_test.components[1].damage_level, damage_vector[1]-self.sys_test.components[1].repair_rate)
        
        # test if the system is not overrepaired
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        self.sys_test.repair()
        for i, component in enumerate(self.sys_test.components):
            self.assertEqual(component.damage_level, 0.0)
            
        damage_vector = np.random.rand(17)
        self.sys_test.set_damage(damage_vector)
        self.sys_test.repair()
        for i, component in enumerate(self.sys_test.components):
            repaired_damage_level = round(damage_vector[i] - component.repair_rate, 5)
            self.assertEqual(component.damage_level, [repaired_damage_level if repaired_damage_level >= 0 else 0.0][0])
        
    def test_update(self):
        self.sys_test.create_system(self.two_comp_sys_wlinks)
        self.sys_test.update()
        for component in self.sys_test.components:
            self.assertEqual(component.functionality_level, 1)
            
        damage_vector = np.multiply(np.ones((5)), 0.4)
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        expected_functionality_levels = [0.6, 0.0, 0.6, 0.0, 0.0]
        for i, component in enumerate(self.sys_test.components):
            self.assertEqual(component.functionality_level, expected_functionality_levels[i])
        
        self.assertEqual(self.sys_test.components[0].supply['utilities'].current['ElectricPower'], 40* 0.6)
        self.assertEqual(self.sys_test.components[1].supply['transfer_services'].current['BridgeTransferService'], 0.0)
        self.assertEqual(self.sys_test.components[2].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8 * 0.6)
        self.assertEqual(self.sys_test.components[3].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.sys_test.components[4].demand['utilities'].current['ElectricPower'], 7.7 * 0.0)
        self.assertEqual(self.sys_test.components[4].demand['utilities'].current['LowLevelCommunication'], 33.3)
        self.assertEqual(self.sys_test.components[4].demand['utilities'].current['PotableWater'], 0.086*0.0)
        self.assertEqual(self.sys_test.components[4].demand['transfer_services'].current['ElectricPowerTransferService'], 7.7 * 0.0)
        self.assertEqual(self.sys_test.components[4].demand['transfer_services'].current['PotableWaterTransferService'], 0.086*0.0)
                         
        
    def test_assemble_system_matrix(self):
        self.sys_test.create_system(self.two_comp_sys_wlinks)
        self.sys_test.assemble_system_matrix()
        # test the initial system matrix 
        epp_vector = [1, 1, 0.0, 1.0, 1]
        epp_supply = [40, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, :5] == epp_vector))   
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 10:15] == epp_supply))
        bridge_vector = [1, 2, 0.0, 1.0, 21]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][1, :5] == bridge_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][1, 5:15] == 0.0))
        bsu_vector = [2, 2, 0, 1, 6]
        bsu_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu_demand = [7.7, 0.0, 33.3, 0.086, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, :5] == bsu_vector))      
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 5:10] == bsu_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 10:15] == bsu_supply))
                
        # test the damaged system matrix 
        damage_vector = [0.4, 0.4, 0.4, 0.4, 0.4]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        epp_vector = [1, 1, 0.4, 0.6, 1]
        epp_supply = [40*0.6, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, :5] == epp_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 10:15] == epp_supply))
        bsu_vector = [2, 2, 0.4, 0.0, 6]
        bsu_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu_demand = [7.7*0.0, 0.0, 33.3, 0.086*0.0, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, :5] == bsu_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 5:10] == bsu_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 10:15] == bsu_supply))
        bridge_vector = [1, 2, 0.4, 0.0, 21]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][1, :5] == bridge_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][1, 5:15] == 0.0))
        # test the system matrix at time step 2 - spike in bsu demand for LLC
        self.sys_test.time_step = 2
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        bsu_demand = [7.7*0.0, 0.0, 33.3*10, 0.086*0.0, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[2][4, 5:10] == bsu_demand))
        # test if the demand met indicators are set to 1
        self.assertTrue(np.all(self.sys_test.system_matrix[0][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))
        
    def test_bridge_service_distribution(self):
        self.sys_test.create_system(self.two_comp_sys_wlinks)
        # test the undamaged system
        self.sys_test.distribute_bridge_transfer_service()
        self.assertEqual(self.sys_test.components[2].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.sys_test.components[3].supply['transfer_services'].current['ElectricPowerTransferService'], 40)
        
        # test when bridge is damaged
        self.sys_test.components[1].damage_level = 0.01
        self.sys_test.update()
        self.assertEqual(self.sys_test.components[1].supply['transfer_services'].current['BridgeTransferService'], 0.0)
        self.sys_test.distribute_bridge_transfer_service()
        self.assertEqual(self.sys_test.components[2].supply['transfer_services'].current['CoolingWaterTransferService'], 0.0)
        self.assertEqual(self.sys_test.components[3].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)    
        
    def test_create_potential_paths(self):
        # create paths from the list of potential paths between two localities
        # test with two comp system
        self.sys_test.create_system(self.two_comp_sys_wlinks)
        # define the dict key as a string from i-th locality to j-th locality, as a list of 
        # localities that the path will go through
        potential_paths = dict()
        potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]]}
        potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]]}
        self.sys_test.set_potential_paths(potential_paths)        
        self.sys_test.create_potential_paths()
        # test create potential paths for undamaged two localities system
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][0][0], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 1'][0][0], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 1'][0][0], Component.EPTL))
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 1 to 2'][0][0], Component.EPTL))
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40)
        # test damaged potential paths - but the bridge is not damaged
        damage_vector = [0.4, 0.0, 0.4, 0.4, 0.4]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.6)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.6)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40*0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40*0.0)
        
        # test when only the bridge is damaged
        damage_vector = [0.0, 0.1, 0.0, 0.0, 0.0]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.distribute_bridge_transfer_service()
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.0)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40*0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40*0.0)
        
        
        # test with a three localities system and multiple potential path between two localities
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        # define the dict key as a string from i-th locality to j-th locality, as a list of 
        # localities that the path will go through
        potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2], [1, 3, 2]], 'from 2 to 1': [[2, 1], [2, 3, 1]],
                                                                        'from 2 to 3': [[2, 1, 3], [2, 3]]}
        potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                                          'from 2 to 3': [[2, 3], [2, 1, 3]], 'from 3 to 2': [[3, 2], [3, 1, 2]]}
        potential_paths['PotableWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                                          'from 2 to 3': [[2, 3], [2, 1, 3]], 'from 3 to 2': [[3, 2], [3, 1, 2]]}
        self.sys_test.set_potential_paths(potential_paths)
        self.sys_test.create_potential_paths()
        # test create potential paths for undamaged two localities system
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][0][0], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][1][0], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][1][1], Component.CWP))
        self.assertEqual(len(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][1]), 2)
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 3'][0][0], Component.CWP))
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 3'][0][1], Component.CWP))
        self.assertEqual(len(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 3'][1]), 1)
        self.assertEqual(len(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 3'][0]), 2)
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 1'][0][0], Component.EPTL))
        self.assertTrue(isinstance(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 1 to 2'][0][0], Component.EPTL))
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40)
        self.assertEqual(self.sys_test.potential_paths_links['PotableWaterTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['PotableWaterTransferService'], 0.8)
        self.assertEqual(self.sys_test.potential_paths_links['PotableWaterTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['PotableWaterTransferService'], 0.8)
        # create the damage vector to test the damaged potential paths
        damage_vector = [0.0, 0.0, 0.0, 0.3, 0.0, 0.4, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.35, 0.0, 0.0, 0.0, 0.0]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        # test the damaged potential paths   - Cooling Water      
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.7)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][1][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.6)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 1 to 2'][1][1].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.65)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.7)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 1'][1][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.65)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 1'][1][1].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.6)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 3'][0][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.7)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 3'][0][1].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.6)
        self.assertEqual(self.sys_test.potential_paths_links['CoolingWaterTransferService']['from 2 to 3'][1][0].supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.65)
        # test the damaged paths - Electric Power
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 1 to 2'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 1'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 3'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 3'][1][0].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 2 to 3'][1][1].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 3 to 2'][0][0].supply['transfer_services'].current['ElectricPowerTransferService'], 40.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 3 to 2'][1][0].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 3 to 2'][1][1].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.sys_test.potential_paths_links['ElectricPowerTransferService']['from 3 to 2'][1][0].supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
    
    def test_get_optimal_path(self):
        # test the algorithm that finds the optimal path from the list of potential paths
        self.sys_test.create_system(self.two_comp_sys_wlinks)
        potential_paths = dict()
        potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]]}
        potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]]} 
        potential_paths['PotableWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]]} 
        self.sys_test.set_potential_paths(potential_paths)
        self.sys_test.create_potential_paths()
        # test the two localities undamaged system
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8)
        self.assertEqual(opt_path, 0)        
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 1, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8)
        self.assertEqual(opt_path, 0)        
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 40)
        self.assertEqual(opt_path, 0)                
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 1, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 40)
        self.assertEqual(opt_path, 0)        
        # test damaged system        
        damage_vector = [0.4, 0.0, 0.4, 0.4, 0.4, 0.0]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8*0.6)
        self.assertEqual(opt_path, 0)        
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 1, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8*0.6)
        self.assertEqual(opt_path, 0)        
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, 0)                
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 1, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, 0)
        
        # test the system with three localities
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        # define the dict key as a string from i-th locality to j-th locality, as a list of 
        # localities that the path will go through
        self.sys_test.potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2], [1, 3, 2]], 'from 2 to 1': [[2, 1], [2, 3, 1]],
                                                                        'from 2 to 3': [[2, 1, 3], [2, 3]]}
        self.sys_test.potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                                          'from 2 to 3': [[2, 3], [2, 1, 3]], 'from 3 to 2': [[3, 2], [3, 1, 2]]}
        self.sys_test.create_potential_paths()
        # test undamaged system
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8)
        self.assertEqual(opt_path, 0)        
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 1, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8)
        self.assertEqual(opt_path, 0)           
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 3, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, None) 
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 3, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8)
        self.assertEqual(opt_path, 0) 
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 40)
        self.assertEqual(opt_path, 0)                
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 1, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 40)
        self.assertEqual(opt_path, 0)
        opt_cost, opt_path = self.sys_test.get_optimal_path(3, 2, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 40)
        self.assertEqual(opt_path, 0) 
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 3, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, None) 
        # create the damage vector to test the damaged potential paths
        damage_vector = [0.0, 0.0, 0.0, 0.3, 0.0, 0.4, 0.01, 0.01, 0.0, 0.0, 0.0, 0.0, 0.35, 0.0, 0.0, 0.0, 0.0]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        # test the damaged potential paths - Cooling Water       
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8*0.7)
        self.assertEqual(opt_path, 0)        
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 1, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8*0.7)
        self.assertEqual(opt_path, 0)           
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 3, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, None) 
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 3, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.65*0.8)
        self.assertEqual(opt_path, 1) 
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, 0)                
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 1, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, 0)
        opt_cost, opt_path = self.sys_test.get_optimal_path(3, 2, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 40)
        self.assertEqual(opt_path, 0) 
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 3, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, None)
        
        # test when the bridge is damaged
        damage_vector = np.zeros(17)
        damage_vector[2] = 0.01
        damage_vector[4] = 0.01
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.distribute_bridge_transfer_service()
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, 0) 
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 2, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, 0)
        opt_cost, opt_path = self.sys_test.get_optimal_path(1, 3, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 0.0)
        self.assertEqual(opt_path, None)
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 3, 'CoolingWaterTransferService')
        self.assertEqual(opt_cost, 0.8)
        self.assertEqual(opt_path, 1)
        opt_cost, opt_path = self.sys_test.get_optimal_path(2, 3, 'ElectricPowerTransferService')
        self.assertEqual(opt_cost, 40)
        self.assertEqual(opt_path, 0)
        
        
    def test_resource_distribution_two_localities(self):            
        # test when system is undamaged
        self.sys_test.create_system(self.two_comp_sys_wlinks)
        self.sys_test.assemble_system_matrix()
        self.sys_test.priorities = Priorities.PrioritiesTwoCompSys()
        self.sys_test.priorities.set_all_priorities(self.sys_test)
        # set the potential paths
        potential_paths = dict()
        potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]]}
        potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]]}
        potential_paths['PotableWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]]}
        self.sys_test.set_potential_paths(potential_paths)
        self.sys_test.create_potential_paths()
        ep_id = 0
        self.sys_test.resource_distribution(ep_id)
        # nothing should change in the system matrix
        epp_vector = [1, 1, 0.0, 1.0, 1]
        epp_supply = [40, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, :5] == epp_vector))   
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 10:15] == epp_supply))
        bsu_vector = [2, 2, 0, 1, 6]
        bsu_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu_demand = [7.7, 0.0, 33.3, 0.086, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, :5] == bsu_vector))      
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 5:10] == bsu_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 10:15] == bsu_supply))   
        # test the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[0][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))
        
        # test when two comp system is damage - the damage is low enough so that the demand is still met        
        damage_vector = [0.4, 0.0, 0.0, 0.0, 0.4]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()            
        self.sys_test.resource_distribution(ep_id)
        epp_vector = [1, 1, 0.4, 0.6, 1]
        epp_supply = [40*0.6, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, :5] == epp_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 10:15] == epp_supply))
        bsu_vector = [2, 2, 0.4, 0.0, 6]
        bsu_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu_demand = [7.7*0.0, 0.0, 33.3, 0.086*0.0, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, :5] == bsu_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 5:10] == bsu_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 10:15] == bsu_supply))     
        # test the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[0][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))
        
        # test when two comp system is damage - the damage is high enough so that the demand is not met
        damage_vector = [0.9, 0.0, 0.0, 0.0, 0.0]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        self.sys_test.resource_distribution(ep_id)
        epp_vector = [1, 1, 0.9, 0.1, 1]
        epp_supply = [40*0.1, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, :5] == epp_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 10:15] == epp_supply))
        bsu_vector = [2, 2, 0, 1, 6]
        bsu_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu_demand = [7.7, 0.0, 33.3, 0.086, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, :5] == bsu_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 5:10] == bsu_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 10:15] == bsu_supply))     
        # test the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))
        # demand met indicator for ep for bsu should be zero
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        
        # test with multiple users and one supplier
        # add one more user to the input dict
        self.two_comp_sys_wlinks[1] = {'LocalityID': 2,
                                'Coord. X': 5,
                                'Coord. Y': 5,
                                'Content': {'BSU': 2},
                                # LinkTo field determines which link types is connected to which locality_id
                                # here locality 1 is connected to locality 2 with one CWP and one EPTL
                                'LinkTo': {'CWP': [1], 'EPTL': [1]},
                                'BridgeTo': {'CWP': [1],
                                           'EPTL': [1],
                                           }} 
        self.sys_test.create_system(self.two_comp_sys_wlinks)
        # recreate potential paths - because the components have changed
        self.sys_test.create_potential_paths()
        # first test with low damage - there should be enough supply
        damage_vector = [0.1, 0.0, 0.0, 0.0, 0.4, 0.3]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        self.sys_test.priorities = Priorities.PrioritiesTwoCompSys()
        self.sys_test.priorities.set_all_priorities(self.sys_test)
        self.sys_test.resource_distribution(ep_id)
        epp_vector = [1, 1, 0.1, 0.9, 1]
        epp_supply = [40*0.9, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, :5] == epp_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 10:15] == epp_supply))
        bsu1_vector = [2, 2, 0.4, 0.0, 6]
        bsu1_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu1_demand = [7.7*0.0, 0.0, 33.3, 0.086*0.0, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, :5] == bsu1_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 5:10] == bsu1_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 10:15] == bsu1_supply))  
        bsu2_vector = [2, 2, 0.3, 1.0, 6]
        bsu2_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu2_demand = [7.7*1.0, 0.0, 33.3, 0.086*1.0, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][5, :5] == bsu2_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][5, 5:10] == bsu2_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][5, 10:15] == bsu2_supply))
        # test the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[0][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))
        # now test with high damage - no user gets enough ep
        damage_vector = [0.9, 0.0, 0.0, 0.0, 0.1, 0.1]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        self.sys_test.resource_distribution(ep_id)
        epp_vector = [1, 1, 0.9, 0.1, 1]
        epp_supply = [40*0.1, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, :5] == epp_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 10:15] == epp_supply))
        bsu1_vector = [2, 2, 0.1, 1.0, 6]
        bsu1_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu1_demand = [7.7*1.0, 0.0, 33.3, 0.086*1.0, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, :5] == bsu1_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 5:10] == bsu1_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4, 10:15] == bsu1_supply))  
        bsu2_vector = [2, 2, 0.1, 1.0, 6]
        bsu2_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu2_demand = [7.7*1.0, 0.0, 33.3, 0.086*1.0, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][5, :5] == bsu2_vector))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][5, 5:10] == bsu2_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][5, 10:15] == bsu2_supply))
        # test the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][4:, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        
        # test with damaged links - damaged CWP
        damage_vector = [0.0, 0.0, 1.0, 0.0, 0.0, 0.0]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix() 
        # distribute power - everything should still be working since only the CWP is damaged
        self.sys_test.resource_distribution(ep_id)
        self.assertTrue(np.all(self.sys_test.system_matrix[0][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))
        # set the damage to the EPTL - minimal damage should still cause a loss of transfer supply
        damage_vector = [0.0, 0.0, 0.0, 0.01, 0.0, 0.0]
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        self.sys_test.resource_distribution(ep_id)
        # the demand of BSUs for power should not be met
        self.assertTrue(np.all(self.sys_test.system_matrix[0][-2:, self.sys_test.system_matrix_demand_met_col_ids[0]] == 0.0))
        # repair the system once and check again - now the EPTL should be functional
        self.sys_test.repair()
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        self.sys_test.resource_distribution(ep_id)
        self.assertTrue(np.all(self.sys_test.system_matrix[0][-2:, self.sys_test.system_matrix_demand_met_col_ids[0]] == 1.0))       
                
        
    def test_resource_distribution_five_components(self):             
        # test with multiple suppliers and multiple users - 5-comp system
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        self.sys_test.assemble_system_matrix()
        self.sys_test.priorities = Priorities.PrioritiesFiveCompSys()
        self.sys_test.priorities.set_all_priorities(self.sys_test)
        potential_paths = dict()
        potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2], [1, 3, 2]], 'from 2 to 1': [[2, 1], [2, 3, 1]],
                                                          'from 1 to 3': [[1, 3], [1, 2, 3]], 'from 3 to 1': [[3, 1], [3, 2, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2], [1, 3, 2]], 'from 2 to 1': [[2, 1], [2, 3, 1]],
                                                          'from 1 to 3': [[1, 3], [1, 2, 3]], 'from 3 to 1': [[3, 1], [3, 2, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        potential_paths['PotableWaterTransferService'] = {'from 1 to 2': [[1, 2], [1, 3, 2]], 'from 2 to 1': [[2, 1], [2, 3, 1]],
                                                          'from 1 to 3': [[1, 3], [1, 2, 3]], 'from 3 to 1': [[3, 1], [3, 2, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        self.sys_test.set_potential_paths(potential_paths)
        self.sys_test.create_potential_paths()
        # distribute all rss 
        ep_id = 0
        self.sys_test.resource_distribution(ep_id)
        llc_id = 2
        self.sys_test.resource_distribution(llc_id)
        cw_id = 4
        self.sys_test.resource_distribution(cw_id)
        # nothing should change in the system matrix - no damage
        # only testing EPP and BSU
        epp_vector = [1, 1, 0.0, 1.0, 1]
        epp_supply = [40, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, :5] == epp_vector))   
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, 10:15] == epp_supply))
        bsu_vector = [3, 3, 0, 1, 6]
        bsu_supply = [0, 0.0, 0.0, 0.0, 0.0]
        bsu_demand = [7.7, 0.0, 33.3, 0.086, 0.0]        
        self.assertTrue(np.all(self.sys_test.system_matrix[0][16, :5] == bsu_vector))      
        self.assertTrue(np.all(self.sys_test.system_matrix[0][16, 5:10] == bsu_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][16, 10:15] == bsu_supply))   
        # test the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[0][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))        
        
        # test with damaged community - EPP is damaged
        damage_vector = np.zeros(len(self.sys_test.components))
        damage_vector[0] = 0.999
        self.sys_test.set_damage(damage_vector)
        self.sys_test.time_step = 2
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        # test the system matrix
        epp_vector = [1, 1, 0.999, 0.001, 1]
        epp_supply = [0.001 * 40, 0.0, 0.0, 0.0, 0.0]
        epp_demand = [0.2, 0.0, 0.001, 0.0, 0.05]  
        self.assertTrue(np.all(self.sys_test.system_matrix[2][0, :5] == epp_vector))   
        self.assertTrue(np.all(self.sys_test.system_matrix[2][0, 5:10] == epp_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[2][0, 10:15] == epp_supply))
        bts_1_vector = [1, 1, 0.0, 1.0, 3]
        bts_1_supply = [0.0, 0.0, 45.0, 0.0, 0.0]
        bts_1_demand = [0.1, 50.0, 0.0, 0.0, 0.0]
        self.assertTrue(np.all(self.sys_test.system_matrix[2][1, :5] == bts_1_vector))   
        self.assertTrue(np.all(self.sys_test.system_matrix[2][1, 5:10] == bts_1_demand))
        self.assertTrue(np.all(self.sys_test.system_matrix[2][1, 10:15] == bts_1_supply))   
        # test rs distribution
        # distribute EP
        ep_id = 0
        self.sys_test.resource_distribution(ep_id, consider_interdep = True)     
        # check the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[2][[0, 1, 10, 15, 16], self.sys_test.system_matrix_demand_met_col_ids[0]] == 0.0))
        
        # test damaged links - damage the bridge from 1 to 2
        damage_vector = np.zeros(len(self.sys_test.components))
        damage_vector[2] = 0.01
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        # distribute EP
        ep_id = 0
        self.sys_test.resource_distribution(ep_id, consider_interdep = True)  
        # because the paths are redundant, even though the bridge is damaged, the demand of all components should be met
        self.assertTrue(np.all(self.sys_test.system_matrix[2][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))      
        
        # damage the CWP from 1 to 2 - nothing should change
        damage_vector = np.zeros(len(self.sys_test.components))
        damage_vector[3] = 1.0
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()       
        # distribute CW
        cw_id = 4
        self.sys_test.resource_distribution(cw_id, consider_interdep = True)
        # test the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[2][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))      
        
        # change potential paths - reduce redundancy
        potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        potential_paths['PotableWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        self.sys_test.set_potential_paths(potential_paths)
        self.sys_test.create_potential_paths()
        # damage the CWP from 1 to 2
        damage_vector = np.zeros(len(self.sys_test.components))
        damage_vector[3] = 1.0
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()  
        # EPP should not get CW - CWP is too damaged
        self.sys_test.resource_distribution(cw_id, consider_interdep = True)
        self.assertTrue(np.all(self.sys_test.system_matrix[2][0, self.sys_test.system_matrix_demand_met_col_ids[cw_id]] == 0.0))   
        
        damage_vector = np.zeros(len(self.sys_test.components))
        damage_vector[3] = 0.5
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        # self.sys_test.create_potential_paths()
        self.sys_test.assemble_system_matrix()  
        # EPP should get CW - CWP is damaged but its transfer supply is still laarger than the demand
        self.sys_test.resource_distribution(cw_id, consider_interdep = True)
        self.assertTrue(np.all(self.sys_test.system_matrix[2][0, self.sys_test.system_matrix_demand_met_col_ids[cw_id]] == 1.0)) 
        
        # damage the bridge from 1 to 2
        damage_vector = np.zeros(len(self.sys_test.components))
        damage_vector[2] = 1.0
        self.sys_test.set_damage(damage_vector)
        self.sys_test.update()
        self.sys_test.distribute_bridge_transfer_service()
        self.sys_test.assemble_system_matrix()
        self.sys_test.resource_distribution(cw_id, consider_interdep = True)
        # EPP should not get CW
        self.assertTrue(np.all(self.sys_test.system_matrix[2][0, self.sys_test.system_matrix_demand_met_col_ids[cw_id]] == 0.0))  
        
        # continue writing test for situations you find out are sketchy
                
    
    def test_get_supply_capacities(self):
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        self.sys_test.assemble_system_matrix()
        expected_supply_caps = [40, 0, 45, 0.2, 0.06]
        supply_capacities = self.sys_test.get_supply_capacities()
        self.assertTrue(np.all(expected_supply_caps == supply_capacities))
        
        # test when system is damaged
        damage_vector = np.zeros(len(self.sys_test.components))
        # damage only the facilities
        damage_vector[0] = 0.5
        damage_vector[1] = 0.1
        damage_vector[10] = 0.5
        damage_vector[15] = 0.1
        self.sys_test.set_damage(damage_vector)      
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()        
        expected_supply_caps = [20, 0.0, 0.0, 0.0, 0.03]
        supply_capacities = np.round(self.sys_test.get_supply_capacities(), 5)
        self.assertTrue(np.all(expected_supply_caps == supply_capacities))
    
    def test_get_total_demand(self):
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        self.sys_test.assemble_system_matrix()
        expected_demands = [8.3, 50, 33.302, 0.086, 0.05]
        total_demand = np.round(self.sys_test.get_total_demand(), 5)        
        self.assertTrue(np.all(expected_demands == total_demand))
        
        # test when system is damaged
        damage_vector = np.zeros(len(self.sys_test.components))
        # damage only the facilities
        damage_vector[0] = 0.5
        damage_vector[1] = 0.1
        damage_vector[10] = 0.5
        damage_vector[15] = 0.1
        damage_vector[16] = 0.1
        self.sys_test.set_damage(damage_vector)      
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        expected_demands = [8.1, 0.0, 33.302, 0.086, 0.05]        
        total_demand = np.round(self.sys_test.get_total_demand(), 5)   
        self.assertTrue(np.all(expected_demands == total_demand))
        
        # test when llc surges
        self.sys_test.time_step = 2
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        expected_demands = [8.1, 0.0, 333.002, 0.086, 0.05]        
        total_demand = np.round(self.sys_test.get_total_demand(), 5)   
        self.assertTrue(np.all(expected_demands == total_demand))
        
    def test_get_total_consumption(self):
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        self.sys_test.assemble_system_matrix()
        expected_cons = [8.3, 50, 33.302, 0.086, 0.05]
        total_cons = np.round(self.sys_test.get_total_consumption(), 5)        
        self.assertTrue(np.all(expected_cons == total_cons))
        
        # test when system is damaged
        damage_vector = np.zeros(len(self.sys_test.components))
        # damage only the facilities
        damage_vector[0] = 0.5
        damage_vector[1] = 0.1
        damage_vector[10] = 0.5
        damage_vector[15] = 0.1
        damage_vector[16] = 0.4
        self.sys_test.set_damage(damage_vector)      
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        self.sys_test.priorities = Priorities.PrioritiesFiveCompSys()
        self.sys_test.priorities.set_all_priorities(self.sys_test)
        # set up potential paths
        potential_paths = dict()
        potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        potential_paths['PotableWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        self.sys_test.set_potential_paths(potential_paths)
        self.sys_test.create_potential_paths()
        ep_id = 0
        self.sys_test.resource_distribution(ep_id, consider_interdep = True)  
        # test consumption after distributing electricity - for this level of damage, all demands should be met
        expected_cons = [0.4, 0.0, 33.302, 0.0, 0.05]
        total_cons = np.round(self.sys_test.get_total_consumption(), 5)        
        self.assertTrue(np.all(expected_cons == total_cons))        
        cw_id = 4
        self.sys_test.resource_distribution(cw_id, consider_interdep = True)
        # test consumption after distributing CW - EPP should not get enough
        expected_cons = [0.4, 0.0, 33.302, 0.0, 0.0]
        total_cons = np.round(self.sys_test.get_total_consumption(), 5)        
        self.assertTrue(np.all(expected_cons == total_cons))       
        # test the consumption after distributing LLC - 
        llc_id = 2
        self.sys_test.resource_distribution(llc_id, consider_interdep = True) 
        expected_cons = [0.4, 0.0, 0.0, 0.0, 0.0]
        total_cons = np.round(self.sys_test.get_total_consumption(), 5)        
        self.assertTrue(np.all(expected_cons == total_cons))       
        
        # test when links are damaged
        
        # damage EPTLs
        damage_vector = np.zeros(len(self.sys_test.components))
        # damage EPTL from 1 to 2
        damage_vector[6] = 0.99
        self.sys_test.set_damage(damage_vector)      
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        # should have no effect on CWF and LLC
        self.sys_test.resource_distribution(cw_id, consider_interdep = True)
        self.sys_test.resource_distribution(llc_id, consider_interdep = True) 
        expected_cons = [8.3, 50, 33.302, 0.086, 0.05]
        total_cons = np.round(self.sys_test.get_total_consumption(), 5)        
        self.assertTrue(np.all(expected_cons == total_cons))
        # should prevent EP from reaching CWF at locality 2
        self.sys_test.resource_distribution(ep_id, consider_interdep = True)
        expected_cons = [8.1, 50, 33.302, 0.086, 0.05]
        total_cons = np.round(self.sys_test.get_total_consumption(), 5)        
        self.assertTrue(np.all(expected_cons == total_cons))
        
        # damage also the EPTL from 2 to 3 - should have no effect
        damage_vector[13] = 0.01
        self.sys_test.set_damage(damage_vector)      
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        self.sys_test.resource_distribution(ep_id, consider_interdep = True)
        expected_cons = [8.1, 50, 33.302, 0.086, 0.05]
        total_cons = np.round(self.sys_test.get_total_consumption(), 5)        
        self.assertTrue(np.all(expected_cons == total_cons))
        
        # damage the EPTL from 1 to 3 - should prevent EP from reaching PWF and BSU
        damage_vector[7] = 0.01
        self.sys_test.set_damage(damage_vector)      
        self.sys_test.update()
        self.sys_test.assemble_system_matrix()
        self.sys_test.resource_distribution(ep_id, consider_interdep = True)
        expected_cons = [0.3, 50, 33.302, 0.086, 0.05]
        total_cons = np.round(self.sys_test.get_total_consumption(), 5)        
        self.assertTrue(np.all(expected_cons == total_cons))       
        
        
    def test_interdependency_modelling(self):
        # add a BSC to the five comp system - to enable the functioning of BTS
        # add one more CWF - to meet the demand of the BSC
        self.five_comp_sys_wlinks[1] = {'LocalityID': 2,
                                'Coord. X': 0,
                                'Coord. Y': 0,
                                'Content': {'CWF': 2,
                                            'BSC': 1},
                                'LinkTo': {'CWP': [1, 3],
                                           'EPTL': [1, 3],
                                           'PWP': [1, 3]},
                                'BridgeTo': {'CWP': [1, 3],
                                           'EPTL': [1, 3]}}
        # test interdependency modelling with the five_comp system
        self.sys_test.create_system(self.five_comp_sys_wlinks)
        self.sys_test.priorities = Priorities.PrioritiesFiveCompSys()
        self.sys_test.priorities.set_all_priorities(self.sys_test)
        # set up potential paths
        potential_paths = dict()
        potential_paths['CoolingWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        potential_paths['ElectricPowerTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        potential_paths['PotableWaterTransferService'] = {'from 1 to 2': [[1, 2]], 'from 2 to 1': [[2, 1]],
                                                          'from 1 to 3': [[1, 3]], 'from 3 to 1': [[3, 1]],
                                                          'from 2 to 3': [[2, 3]], 'from 3 to 2': [[3, 2]]}
        self.sys_test.set_potential_paths(potential_paths)
        self.sys_test.create_potential_paths()
        self.sys_test.interdependency_modelling(consider_interdep = True)
        # there should be enough supply for all components - check the demand met columns
        self.assertTrue(np.all(self.sys_test.system_matrix[0][:, self.sys_test.system_matrix_demand_met_col_ids] == 1.0))
        
        # damage the bridge from 1 to 3 - should prevent the functionality of PWF and BSU
        damage_vector = np.zeros(len(self.sys_test.components))
        # damage EPTL from 1 to 2
        damage_vector[4] = 0.1
        self.sys_test.set_damage(damage_vector)      
        self.sys_test.update()
        self.sys_test.interdependency_modelling(consider_interdep = True)
        # BSU should have no power and potable water
        ep_id = 0
        pw_id = 3        
        self.assertTrue(np.all(self.sys_test.system_matrix[0][18, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][18, self.sys_test.system_matrix_demand_met_col_ids[pw_id]] == 0.0))
        # PWF should have no power
        self.assertTrue(np.all(self.sys_test.system_matrix[0][17, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        
        # damage the CWP from 1 to 2 - should prevent the EPP from getting CWF and cause chaos (components do not have power)
        damage_vector = np.zeros(len(self.sys_test.components))   
        damage_vector[3] = 0.99 # CWP will have a transfer capacity of 0.008
        self.sys_test.set_damage(damage_vector)      
        self.sys_test.update()
        self.sys_test.interdependency_modelling(consider_interdep = True)
        # test whether the demands are met
        cw_id = 4
        llc_id = 2
        hlc_id = 1
        # EPP should not get CW, and therefore the BSC won't get power and EPP won't also get LLC
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, self.sys_test.system_matrix_demand_met_col_ids[cw_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][0, self.sys_test.system_matrix_demand_met_col_ids[llc_id]] == 0.0))
        # BTS should not get power and HLC
        self.assertTrue(np.all(self.sys_test.system_matrix[0][1, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][1, self.sys_test.system_matrix_demand_met_col_ids[hlc_id]] == 0.0))
        # BSC should not get EP and CW
        self.assertTrue(np.all(self.sys_test.system_matrix[0][12, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][12, self.sys_test.system_matrix_demand_met_col_ids[cw_id]] == 0.0))
        # CWFs should not get EP and LLC
        self.assertTrue(np.all(self.sys_test.system_matrix[0][10, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][10, self.sys_test.system_matrix_demand_met_col_ids[llc_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][11, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][11, self.sys_test.system_matrix_demand_met_col_ids[llc_id]] == 0.0))
        # PWF should not get EP 
        self.assertTrue(np.all(self.sys_test.system_matrix[0][17, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        # BSU should not get EP, LLC and PW
        self.assertTrue(np.all(self.sys_test.system_matrix[0][18, self.sys_test.system_matrix_demand_met_col_ids[ep_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][18, self.sys_test.system_matrix_demand_met_col_ids[llc_id]] == 0.0))
        self.assertTrue(np.all(self.sys_test.system_matrix[0][18, self.sys_test.system_matrix_demand_met_col_ids[pw_id]] == 0.0))
        
    def test_check_recovery_target(self):
        self.sys_test.create_system(self.five_comp_sys)
        # when initialized the recovery traget should be met - all components are initialized with 0 damage level
        self.assertTrue(self.sys_test.check_recovery_target())
        
        # test when system is damaged
        damage_vector = np.zeros(len(self.sys_test.components))
        # damage one facility
        damage_vector[0] = 0.5
        
        self.sys_test.set_damage(damage_vector)     
        self.sys_test.update() 
        self.assertTrue(not(self.sys_test.check_recovery_target()))
        
        # repair the system and then test the condition - assumed repair rate is 0.1, so it recovers in 4 time steps
        for i in range(50):
            self.sys_test.repair()
                   
        self.assertTrue(self.sys_test.check_recovery_target())
             
#     def test_recovery_simulation(self):
#         self.sys_test.create_system(self.five_comp_sys)
#         self.sys_test.priorities = Priorities.PrioritiesFiveCompSys()
#         self.sys_test.priorities.set_all_priorities(self.sys_test)
#         damage_vector = [0.4, 0.0, 0.4, 0.4, 0.4]
#         self.sys_test.recovery_simulation(damage_vector, plot_LoR=False)
#         self.assertEqual(len(self.sys_test.system_matrix), 7)        
#         # TODO: Implement more tests - test the system matrix at each time_step!
       

#     def test_calculate_LoR(self):
#         self.sys_test.create_system(self.five_comp_sys)
#         self.sys_test.priorities = Priorities.PrioritiesFiveCompSys()
#         self.sys_test.priorities.set_all_priorities(self.sys_test)
#         damage_vector = [0.4, 0.0, 0.4, 0.4, 0.4]
#         self.sys_test.recovery_simulation(damage_vector, plot_LoR = False)
        
#         # TODO: test the LoR values for the five component community without links
        
#     def test_create_links(self):
#         self.sys_test.create_system(self.two_comp_sys_wlinks)        
#         cwp = [self.sys_test.components[i] for i,component in enumerate(self.sys_test.components) if type(component)==Component.CWP]
#         eptl = [self.sys_test.components[i] for i,component in enumerate(self.sys_test.components) if type(component)==Component.EPTL]
#         # check if there is only one CWP - there is no duplication of links
#         self.assertEqual(len(cwp), 1)
#         self.assertEqual(len(eptl), 1)
#         # check link type  
#         # get the variables from the list
#         cwp = cwp[0]
#         eptl = eptl[0]
#         self.assertTrue(Component.CWP == type(cwp))
#         self.assertTrue(Component.EPTL == type(eptl))
#         self.assertTrue(cwp.start_locality == 1)
#         self.assertTrue(cwp.end_locality == 2)
#         self.assertTrue(eptl.start_locality == 1)
#         self.assertTrue(eptl.end_locality == 2)
#         # TODO: Test with five comp system
        
#     def test_assemble_transfer_supply_matrix(self):
#         self.sys_test.create_system(self.two_comp_sys_wlinks)
#         self.sys_test.assemble_transfer_supply_matrix()
#         transfer_supply_matrix = self.sys_test.transfer_supply_matrix[0]
#         # test whether the matrix picked up all the considered transfer services
#         self.assertTrue(np.all([transfer_service in transfer_supply_matrix for transfer_service in self.sys_test.considered_transfer_services]))
#         self.assertTrue(np.shape(transfer_supply_matrix['ElectricPowerTransferService']) == (2, 2))
#         # test whether diagonal values are infinite
#         self.assertTrue(np.all([transfer_supply_matrix['ElectricPowerTransferService'][0, 0] == math.inf,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][1, 1] == math.inf]))
#         # test offdiagonal values
#         self.assertTrue(np.all([transfer_supply_matrix['ElectricPowerTransferService'][0, 1] == 5,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][1, 0] == 5]))
#         # test the offdiagonal values
#         self.assertTrue(np.all([transfer_supply_matrix['CoolingWaterTransferService'][0, 1] == 3,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][1, 0] == 3]))
#         # test five comp sys with links
#         self.sys_test.create_system(self.five_comp_sys_wlinks)
#         self.sys_test.assemble_transfer_supply_matrix()
#         transfer_supply_matrix = self.sys_test.transfer_supply_matrix[0]
#         self.assertTrue(np.shape(transfer_supply_matrix['ElectricPowerTransferService']) == (3, 3))
#         # test offdiagonal values
#         self.assertTrue(np.all([transfer_supply_matrix['ElectricPowerTransferService'][0, 1] == 5,                              
#                                 transfer_supply_matrix['ElectricPowerTransferService'][1, 0] == 5,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][2, 0] == 5,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][0, 2] == 5,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][1, 2] == 5,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][2, 1] == 5,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][0, 0] == math.inf,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][1, 1] == math.inf,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][2, 2] == math.inf]))
#         # test the offdiagonal values
#         self.assertTrue(np.all([transfer_supply_matrix['CoolingWaterTransferService'][0, 1] == 3,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][1, 0] == 3]))
        
#         # test when system is damaged
#         # set all components to 0.4 damage level
#         damage_vector = [0.4 for _ in self.sys_test.components]
#         self.sys_test.set_damage(damage_vector)
#         self.sys_test.update()
#         self.sys_test.assemble_transfer_supply_matrix()
#         transfer_supply_matrix = self.sys_test.transfer_supply_matrix[0]
#         # test EPTLs - binary links
#         self.assertTrue(np.all([transfer_supply_matrix['ElectricPowerTransferService'][0, 1] == 0,                              
#                                 transfer_supply_matrix['ElectricPowerTransferService'][1, 0] == 0,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][2, 0] == 0,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][0, 2] == 0,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][1, 2] == 0,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][2, 1] == 0,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][0, 0] == math.inf,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][1, 1] == math.inf,
#                                 transfer_supply_matrix['ElectricPowerTransferService'][2, 2] == math.inf]))
        
#         # test CWPs - linear links
#         self.assertTrue(np.all([transfer_supply_matrix['CoolingWaterTransferService'][0, 1] == 3*0.6,                              
#                                 transfer_supply_matrix['CoolingWaterTransferService'][1, 0] == 3*0.6,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][2, 0] == 3*0.6,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][0, 2] == 3*0.6,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][1, 2] == 3*0.6,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][2, 1] == 3*0.6,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][0, 0] == math.inf,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][1, 1] == math.inf,
#                                 transfer_supply_matrix['CoolingWaterTransferService'][2, 2] == math.inf]))

# =============================================================================
#     def test_interdependency_modelling_irecodes_small_example(self):
#         # TODO: Needs to be properly initialized - component properties need to be set
#         # test damaged system
#         damage_vector = [0.4, 0.0, 0.4, 0.4, 0.4]
#         self.sys_test.set_damage(damage_vector)
#         self.sys_test.time_step = 2
#         self.sys_test.update()        
#         self.sys_test.interdependency_modelling()
#         # test the system matrix - following the example from the iReCoDeS paper
#         epp_vector = [1, 1, 0.4, 0.6, 1]
#         epp_supply = [0.0, 0.0, 0.0, 0.0, 0.0]
#         epp_demand = [0.0, 0.0, 1.0, 0.0, 1.0]  
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][0, :5] == epp_vector))   
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][0, 5:10] == epp_demand))
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][0, 10:15] == epp_supply))
#         bts_1_vector = [1, 1, 0.0, 1.0, 3]
#         bts_1_supply = [0.0, 0.0, 0.0, 0.0, 0.0]
#         bts_1_demand = [1.0, 0.0, 0.0, 0.0, 0.0]
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][1, :5] == bts_1_vector))   
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][1, 5:10] == bts_1_demand))
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][1, 10:15] == bts_1_supply))
#         cwf_vector = [2, 2, 0.4, 0.6, 5]
#         cwf_supply = [0.0, 0.0, 0.0, 0.0, 0.0]
#         cwf_demand = [1.0, 0.0, 1.0, 0.0, 0.0]        
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][2, :5] == cwf_vector))   
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][2, 5:10] == cwf_demand))
#         self.assertTrue(np.all(np.round(self.sys_test.system_matrix[2][2, 10:15], 10) == cwf_supply))
#         bts_2_vector = [3, 3, 0.4, 0.0, 4]
#         bts_2_supply = [0.0, 0.0, 0.0, 0.0, 0.0]
#         bts_2_demand = [0.0, 0.0, 0.0, 0.0, 0.0]
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][3, :5] == bts_2_vector))   
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][3, 5:10] == bts_2_demand))
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][3, 10:15] == bts_2_supply))
#         bsu_vector = [3, 3, 0.4, 0.6, 6]
#         bsu_supply = [0.0, 0.0, 0.0, 0.0, 0.0]
#         bsu_demand = [0.6, 0.0, 10.0, 0.0, 0.0]
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][4, :5] == bsu_vector))   
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][4, 5:10] == bsu_demand))
#         self.assertTrue(np.all(self.sys_test.system_matrix[2][4, 10:15] == bsu_supply))       
# =============================================================================
     
# # =============================================================================
# #     def test_lca(self):
# #         # TODO: Fix the LCA implementation and tests
# #         # test the implementation of the Label Correcting Algorithm
# #         self.sys_test.create_system(self.two_comp_sys_wlinks)
# #         transfer_supply_matrix = dict()
# #         transfer_supply_matrix['transfer_service_1'] = np.asarray([[math.inf, 10], [10, math.inf]]) 
# #         self.sys_test.transfer_supply_matrix[0] = transfer_supply_matrix
# #         optCost, optPath = self.sys_test.lca(1, 2, 'transfer_service_1')   
# #         self.assertEqual(optCost, -10)
# #         self.assertEqual(optPath, [1, 2])
# #         
# #         # test with three localities
# #         self.sys_test.create_system(self.five_comp_sys_wlinks)
# #         transfer_supply_matrix = dict()
# #         transfer_supply_matrix['transfer_service_1'] = np.asarray([[math.inf, 10, 5], [10, math.inf, 0], [5, 0, math.inf]]) 
# #         self.sys_test.transfer_supply_matrix[0] = transfer_supply_matrix
# #         optCost, optPath = self.sys_test.lca(1, 2, 'transfer_service_1') 
# #         self.assertEqual(optCost, -10)
# #         self.assertEqual(optPath, [1, 2])
# #         
# #         optCost, optPath = self.sys_test.lca(1, 3, 'transfer_service_1') 
# #         self.assertEqual(optCost, -5)
# #         self.assertEqual(optPath, [1, 3])
# #         
# #         optCost, optPath = self.sys_test.lca(2, 3, 'transfer_service_1') 
# #         self.assertEqual(optCost, -5.0)
# #         self.assertEqual(optPath, [2, 1, 3])
# #         
# #         # test with six localities
# #         self.sys_test.create_system(self.five_comp_sys_wlinks)
# #         # create a dummy sys with imaginery six localities
# #         self.sys_test.num_localities = 6
# #         transfer_supply_matrix = dict()
# #         transfer_supply_matrix['transfer_service_1'] = np.array([[math.inf, 5, 10, 20, 0, 0], 
# #                                                                    [5, math.inf, 0, 10, 5, 0],
# #                                                                    [10, 0, math.inf, 0, 15, 0],
# #                                                                    [20, 10, 0, math.inf, 0, 0],
# #                                                                    [0, 5, 15, 0, math.inf, 30],
# #                                                                    [0, 0, 0, 0, 30, math.inf]]).reshape((6, 6)) 
# #         
# #         self.sys_test.transfer_supply_matrix[0] = transfer_supply_matrix
# #         optCost, optPath = self.sys_test.lca(1, 2, 'transfer_service_1') 
# #         self.assertEqual(optCost, -10.0)
# #         self.assertEqual(optPath, [1, 4, 2])
# #         
# #         optCost, optPath = self.sys_test.lca(1, 3, 'transfer_service_1') 
# #         self.assertEqual(optCost, -10.0)
# #         self.assertEqual(optPath, [1, 3])
# #         
# #         optCost, optPath = self.sys_test.lca(1, 4, 'transfer_service_1') 
# #         self.assertEqual(optCost, -20.0)
# #         self.assertEqual(optPath, [1, 4])
# #         
# #         optCost, optPath = self.sys_test.lca(1, 5, 'transfer_service_1') 
# #         self.assertEqual(optCost, -10.0)
# #         self.assertEqual(optPath, [1, 3, 5])
# # =============================================================================
        
        
  
    
    
    
    
if __name__ == '__main__':
    unittest.main()       
