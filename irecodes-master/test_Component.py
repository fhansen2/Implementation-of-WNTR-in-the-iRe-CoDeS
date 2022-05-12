# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:08:15 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""
import unittest
import Component
import numpy as np
import RSGroup
import System

# Add more checks as you notice issues
class TestComponent(unittest.TestCase):
    
    def setUp(self):
        self.comp_1 = Component.Component(1, 2)
        self.rs_list_1 = RSGroup.OrderedDefaultDict([('rs1', 5),
                                                  ('rs2', 4),
                                                  ('rs3', 3)])    
        self.one_comp_sys = {}
        self.considered_utilities = ['ElectricPower', 'HighLevelCommunication',
                                     'LowLevelCommunication', 'PotableWater', 
                                     'CoolingWater']
        self.considered_transfer_services = ['PowerLine', 'Pipe']
        self.one_comp_sys = [dict()]
        self.one_comp_sys[0] = {'LocalityID': 1,
                                'Coord. X': 0,
                                'Coord. Y': 0,
                                'Content': {'EPP': 1}} 
        self.sys_test = System.System(self.considered_utilities, self.considered_transfer_services)    
        self.sys_test.create_system(self.one_comp_sys)
    def test_constructor(self):        
        self.assertEqual(self.comp_1.start_locality, 1)
        self.assertEqual(self.comp_1.end_locality, 2)        
        
    def test_set_damage(self):
        damage = 0.3
        self.comp_1.set_damage(damage)
        self.assertEqual(self.comp_1.damage_level, damage)
        
    def test_update_func(self):
        damage = 0.3
        self.comp_1.set_damage(damage)
        # by default component takes linear dam-func relation
        self.comp_1.update_func()
        self.assertEqual(self.comp_1.functionality_level, 0.7)
        
    def test_add_initial_supply_rs_group(self):
        self.comp_1.add_initial_supply_rs_group('utilities', self.rs_list_1)
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs1'], 5)
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs2'], 4)
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs3'], 3)
        # check if non existant rs returns zeros
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs!'], 0)
        # current values should be the same as initial, when initial values are set        
        self.assertEqual(self.comp_1.supply['utilities'].current['rs1'], 5)
        self.assertEqual(self.comp_1.supply['utilities'].current['rs2'], 4)
        self.assertEqual(self.comp_1.supply['utilities'].current['rs3'], 3)
        # check if non existant rs returns zeros
        self.assertEqual(self.comp_1.supply['utilities'].current['rs!'], 0)
            
    def test_add_initial_demand_rs_group(self):
        self.comp_1.add_initial_demand_rs_group('utilities', self.rs_list_1)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs1'], 5)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs2'], 4)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs3'], 3)
        # check if non existant rs returns zeros
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs!'], 0)
        # current values should be the same as initial, when initial values are set        
        self.assertEqual(self.comp_1.demand['utilities'].current['rs1'], 5)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs2'], 4)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs3'], 3)
        # check if non existant rs returns zeros
        self.assertEqual(self.comp_1.demand['utilities'].current['rs!'], 0)
        
    def test_update_supply(self):             
        self.comp_1.add_initial_supply_rs_group('utilities', self.rs_list_1)
        damage = 0.3
        self.comp_1.set_damage(damage)
        self.comp_1.update_func()
        self.comp_1.update_supply()
        # by default a component is a linear supplier
        self.assertEqual(self.comp_1.supply['utilities'].current['rs1'], self.rs_list_1['rs1'] * 0.7)
        self.assertEqual(self.comp_1.supply['utilities'].current['rs2'], self.rs_list_1['rs2'] * 0.7)
        self.assertEqual(self.comp_1.supply['utilities'].current['rs3'], self.rs_list_1['rs3'] * 0.7)
        # non existant fileds should be zero
        self.assertEqual(self.comp_1.supply['utilities'].current['rs!'], 0)
        # initial values should not change
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs1'], self.rs_list_1['rs1'] * 1.0)
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs2'], self.rs_list_1['rs2'] * 1.0)
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs3'], self.rs_list_1['rs3'] * 1.0)
        # non existant fileds should be zero
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs!'], 0)
        
    def test_update_demand(self):        
        self.comp_1.add_initial_demand_rs_group('utilities', self.rs_list_1)
        damage = 0.3
        self.comp_1.set_damage(damage)
        self.comp_1.update_func()
        self.comp_1.update_demand()
        self.assertEqual(self.comp_1.demand['utilities'].current['rs1'], self.rs_list_1['rs1'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs2'], self.rs_list_1['rs2'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs3'], self.rs_list_1['rs3'] * 1.0)
         # non existant fileds should be zero
        self.assertEqual(self.comp_1.demand['utilities'].current['rs!'], 0)
        # initial values should not change
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs1'], self.rs_list_1['rs1'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs2'], self.rs_list_1['rs2'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs3'], self.rs_list_1['rs3'] * 1.0)
        # non existant fileds should be zero
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs!'], 0)
        # test if the demand is zero when func level is zero
        self.comp_1.set_damage(1)
        self.comp_1.update_func()
        self.comp_1.update_demand()
        self.assertEqual(self.comp_1.demand['utilities'].current['rs1'], self.rs_list_1['rs1'] * 0.0)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs2'], self.rs_list_1['rs2'] * 0.0)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs3'], self.rs_list_1['rs3'] * 0.0)
         # non existant fileds should be zero
        self.assertEqual(self.comp_1.demand['utilities'].current['rs!'], 0)
        # initial values should not change
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs1'], self.rs_list_1['rs1'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs2'], self.rs_list_1['rs2'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs3'], self.rs_list_1['rs3'] * 1.0)
  
    def test_update(self):        
        self.comp_1.add_initial_supply_rs_group('utilities', self.rs_list_1)
        self.comp_1.add_initial_demand_rs_group('utilities', self.rs_list_1)
        damage = 0.3
        self.comp_1.set_damage(damage)
        self.comp_1.update()
        self.assertEqual(self.comp_1.functionality_level, 0.7)
        # test current values
        self.assertEqual(self.comp_1.supply['utilities'].current['rs1'], self.rs_list_1['rs1'] * 0.7)
        self.assertEqual(self.comp_1.supply['utilities'].current['rs2'], self.rs_list_1['rs2'] * 0.7)
        self.assertEqual(self.comp_1.supply['utilities'].current['rs3'], self.rs_list_1['rs3'] * 0.7)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs1'], self.rs_list_1['rs1'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs2'], self.rs_list_1['rs2'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].current['rs3'], self.rs_list_1['rs3'] * 1.0)
        # test initial values
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs1'], self.rs_list_1['rs1'] * 1.0)
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs2'], self.rs_list_1['rs2'] * 1.0)
        self.assertEqual(self.comp_1.supply['utilities'].initial['rs3'], self.rs_list_1['rs3'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs1'], self.rs_list_1['rs1'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs2'], self.rs_list_1['rs2'] * 1.0)
        self.assertEqual(self.comp_1.demand['utilities'].initial['rs3'], self.rs_list_1['rs3'] * 1.0)
       
       
    def test_check_demand_indicators(self):
        matrix = np.ones([5, 4]) 
        comp_num = 2
        func_columns = [1, 2, 3]
        func_indicator = self.comp_1.check_demand_indicators(matrix, comp_num, func_columns)       
        self.assertTrue(func_indicator)
        
        damage = 0.4
        self.comp_1.set_damage(damage)
        func_indicator = self.comp_1.check_demand_indicators(matrix, comp_num, func_columns)
        self.assertTrue(func_indicator)
        
        damage = 1.0
        self.comp_1.set_damage(damage)
        matrix[comp_num, func_columns[1]] = 0
        func_indicator = self.comp_1.check_demand_indicators(matrix, comp_num, func_columns)
        self.assertFalse(func_indicator)
        
    def test_collect_general_properties(self):
        self.comp_1.set_damage(0.3)
        self.comp_1.id = 8
        self.comp_1.update()
        general_props = self.comp_1.collect_general_properties(self.sys_test)
        self.assertTrue(np.all(general_props == [1, 2, 0.3, 0.7, 8]))
        
    def test_repair(self):
        self.comp_1.set_damage(0.3)
        self.comp_1.repair_rate = 0.1
        self.comp_1.repair()
        self.assertEqual(round(self.comp_1.damage_level, 4), 0.2)        
    
    def test_collect_rs_demand_supply_values(self):
        self.comp_1.add_initial_supply_rs_group('utilities', self.rs_list_1)
        self.comp_1.add_initial_demand_rs_group('utilities', self.rs_list_1)
        initial_vector = self.comp_1.collect_rs_demand_supply_values('utilities', self.rs_list_1)
        self.assertTrue(np.all(initial_vector == [5, 4, 3, 5, 4, 3]))
        # test if it works when component is damage
        self.comp_1.set_damage(0.3)
        self.comp_1.update()
        updated_vector = self.comp_1.collect_rs_demand_supply_values('utilities', self.rs_list_1)
        self.assertTrue(np.all(updated_vector == [5, 4, 3, 5*0.7, 4*0.7, 3*0.7]))
                   

# test Electric Power Plant class
class TestEPP(unittest.TestCase):        
    
    def setUp(self):
        # create an EEP component to test
        self.EPP = Component.EPP(1, 1)
        
    def test_constructor(self):
        # test EPP properties
        self.assertEqual(self.EPP.id, 1)
        self.assertEqual(self.EPP.repair_rate, 0.01)
        self.assertEqual(self.EPP.supply['utilities'].initial['ElectricPower'],40)
        self.assertEqual(self.EPP.demand['utilities'].initial['LowLevelCommunication'], 0.001)
        self.assertEqual(self.EPP.demand['utilities'].initial['CoolingWater'], 0.05)
        self.assertEqual(self.EPP.demand['transfer_services'].initial['CoolingWaterTransferService'], 0.05)
        
    def test_update_func(self):
        self.EPP.set_damage(0.4)
        self.EPP.update_func()
        self.assertEqual(self.EPP.functionality_level, 0.6)
        
    def test_update(self):
        self.EPP.set_damage(0.4)
        self.EPP.update()
        self.assertEqual(self.EPP.supply['utilities'].current['ElectricPower'], 40*0.6)
        self.assertEqual(self.EPP.demand['utilities'].current['LowLevelCommunication'], 0.001)
        self.assertEqual(self.EPP.demand['utilities'].current['CoolingWater'], 0.05)
        self.assertEqual(self.EPP.demand['transfer_services'].current['CoolingWaterTransferService'], 0.05)
        # test when func level is zero
        self.EPP.set_damage(1.0)
        self.EPP.update()
        self.assertEqual(self.EPP.supply['utilities'].current['ElectricPower'], 0.0)
        self.assertEqual(self.EPP.demand['utilities'].current['LowLevelCommunication'], 0.0)
        self.assertEqual(self.EPP.demand['utilities'].current['CoolingWater'], 0.0)
        self.assertEqual(self.EPP.demand['transfer_services'].current['CoolingWaterTransferService'], 0.0)
        
# test Building Stock Unit class
class TestBSU(unittest.TestCase):  
    
    def setUp(self):
        self.BSU = Component.BSU(1, 1)
        self.dummy_sys = System.System([], [])        

    def test_constructor(self):
        # test EPP properties
        self.assertEqual(self.BSU.id, 6)
        self.assertEqual(self.BSU.repair_rate, 0.01)
        # test demand values
        self.assertEqual(self.BSU.demand['utilities'].initial['LowLevelCommunication'], 33.3)
        self.assertEqual(self.BSU.demand['utilities'].initial['ElectricPower'], 7.7)
        self.assertEqual(self.BSU.demand['utilities'].initial['PotableWater'], 0.086)
        self.assertEqual(self.BSU.demand['transfer_services'].initial['PotableWaterTransferService'], 0.086)
        self.assertEqual(self.BSU.demand['transfer_services'].initial['ElectricPowerTransferService'], 7.7)
        
    def test_update_func(self):
        self.BSU.set_damage(0.4)
        self.BSU.update_func()
        self.assertEqual(self.BSU.functionality_level, 0.0)
        
        self.BSU.set_damage(0.1)
        self.BSU.update_func()
        self.assertEqual(self.BSU.functionality_level, 1.0)
        
    def test_update(self):
        self.BSU.set_damage(0.2)           
        self.BSU.update(self.dummy_sys)
        self.assertEqual(self.BSU.demand['utilities'].current['LowLevelCommunication'], 33.3)
        self.assertEqual(self.BSU.demand['utilities'].current['ElectricPower'], 7.7)
        self.assertEqual(self.BSU.demand['utilities'].current['PotableWater'], 0.086)
        self.assertEqual(self.BSU.demand['transfer_services'].current['PotableWaterTransferService'], 0.086)
        self.assertEqual(self.BSU.demand['transfer_services'].current['ElectricPowerTransferService'], 7.7)
        # test when func level is zero
        self.BSU.set_damage(1.0)
        self.BSU.update(self.dummy_sys)        
        self.assertEqual(self.BSU.demand['utilities'].current['LowLevelCommunication'], 33.3)
        self.assertEqual(self.BSU.demand['utilities'].current['ElectricPower'], 0.0)
        self.assertEqual(self.BSU.demand['utilities'].current['PotableWater'], 0.0)
        self.assertEqual(self.BSU.demand['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.BSU.demand['transfer_services'].current['PotableWaterTransferService'], 0.0)
        # test LLC demand when time step is 2 and the BSU is not damaged
        self.BSU.set_damage(0.0)
        self.dummy_sys.time_step = 2
        self.BSU.update(self.dummy_sys)
        self.assertEqual(self.BSU.demand['utilities'].current['LowLevelCommunication'], 33.3)
        # test LLC demand when time step is 2 and the BSU is damaged
        self.BSU.set_damage(0.1)
        self.dummy_sys.time_step = 2
        self.BSU.update(self.dummy_sys)
        self.assertEqual(self.BSU.demand['utilities'].current['LowLevelCommunication'], 33.3*10)

# test Base Station Controller
class TestBSC(unittest.TestCase):
    
    def setUp(self):
        self.BSC = Component.BSC(1, 1)
        self.dummy_sys = System.System([], [])
                    
    def test_constructor(self):
        # test BSC properties
        self.assertEqual(self.BSC.id, 2)
        self.assertEqual(self.BSC.repair_rate, 0.01)
        self.assertEqual(self.BSC.supply['utilities'].initial['HighLevelCommunication'], 300)
        self.assertEqual(self.BSC.supply['utilities'].initial['LowLevelCommunication'], 0)
        self.assertEqual(self.BSC.demand['utilities'].initial['ElectricPower'], 0.2)
        self.assertEqual(self.BSC.demand['utilities'].initial['LowLevelCommunication'], 0.0)
        self.assertEqual(self.BSC.demand['utilities'].initial['CoolingWater'], 0.05)
        self.assertEqual(self.BSC.demand['transfer_services'].initial['ElectricPowerTransferService'], 0.2)
        self.assertEqual(self.BSC.demand['transfer_services'].initial['CoolingWaterTransferService'], 0.05)

    def test_update(self):
        self.BSC.damage_level = 0.4
        self.BSC.update(self.dummy_sys)
        self.assertEqual(self.BSC.functionality_level, 0.6)
        self.assertEqual(self.BSC.supply['utilities'].initial['HighLevelCommunication'], 300)
        self.assertEqual(self.BSC.supply['utilities'].current['HighLevelCommunication'], 300*0.6)
        self.assertEqual(self.BSC.demand['utilities'].current['ElectricPower'], 0.2)
        self.assertEqual(self.BSC.demand['utilities'].current['LowLevelCommunication'], 0.0)
        self.assertEqual(self.BSC.demand['utilities'].current['CoolingWater'], 0.05)
        self.assertEqual(self.BSC.demand['transfer_services'].current['ElectricPowerTransferService'], 0.2)
        self.assertEqual(self.BSC.demand['transfer_services'].current['CoolingWaterTransferService'], 0.05)
        
        self.BSC.damage_level = 1.0
        self.BSC.update(self.dummy_sys)
        self.assertEqual(self.BSC.functionality_level, 0.0)
        self.assertEqual(self.BSC.supply['utilities'].initial['HighLevelCommunication'], 300)
        self.assertEqual(self.BSC.supply['utilities'].current['HighLevelCommunication'], 300*0.0)
        self.assertEqual(self.BSC.demand['utilities'].current['ElectricPower'], 0.0)
        self.assertEqual(self.BSC.demand['utilities'].current['LowLevelCommunication'], 0.0)
        self.assertEqual(self.BSC.demand['utilities'].current['CoolingWater'], 0.0)
        self.assertEqual(self.BSC.demand['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.BSC.demand['transfer_services'].current['CoolingWaterTransferService'], 0.0)
        
# test Electric Power Transmission Line
class TestEPTL(unittest.TestCase):

    def setUp(self):
        self.EPTL = Component.EPTL(1, 2)
        self.dummy_sys = System.System([], [])
        self.EPTL_on_bridge = Component.EPTL(1, 2, bridge=True)
        self.Bridge = Component.Bridge(1, 2)
    
    def test_constructor(self):
        self.assertEqual(self.EPTL.id, 11)
        self.assertEqual(self.EPTL.repair_rate, 0.05)
        self.assertEqual(self.EPTL.supply['transfer_services'].current['ElectricPowerTransferService'], 40)
        self.assertEqual(self.EPTL.supply['utilities'].current['ElectricPower'], 0.0)
        self.assertEqual(self.EPTL.demand['transfer_services'].current['BridgeTransferService'], 0.0)
        
        self.assertEqual(self.EPTL_on_bridge.supply['transfer_services'].current['ElectricPowerTransferService'], 40)
        self.assertEqual(self.EPTL_on_bridge.supply['utilities'].current['ElectricPower'], 0.0)
        self.assertEqual(self.EPTL_on_bridge.demand['transfer_services'].current['BridgeTransferService'], 1.0)
        
    def test_update(self):
        self.EPTL.damage_level = 0.01
        self.EPTL_on_bridge.damage_level = 0.01
        self.EPTL.update(self.dummy_sys)
        self.EPTL_on_bridge.update(self.dummy_sys)
        self.assertEqual(self.EPTL.functionality_level, 0.0)
        self.assertEqual(self.EPTL.supply['transfer_services'].current['ElectricPowerTransferService'], 0.0)
        self.assertEqual(self.EPTL_on_bridge.demand['transfer_services'].current['BridgeTransferService'], 0.0)        
        
        
# test Cooling Water Pipes    
class TestCWP(unittest.TestCase):

    def setUp(self):
        self.CWP = Component.CWP(1, 2)
        self.dummy_sys = System.System([], [])
        self.CWP_on_bridge = Component.CWP(1, 2, bridge=True)
        
    def test_constructor(self):
        self.assertEqual(self.CWP.id, 15)
        self.assertEqual(self.CWP.repair_rate, 0.05)
        self.assertEqual(self.CWP_on_bridge.id, 15)
        self.assertEqual(self.CWP_on_bridge.repair_rate, 0.05)
        self.assertEqual(self.CWP.supply['transfer_services'].initial['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.CWP_on_bridge.supply['transfer_services'].initial['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.CWP.demand['transfer_services'].initial['BridgeTransferService'], 0.0)
        self.assertEqual(self.CWP_on_bridge.demand['transfer_services'].initial['BridgeTransferService'], 1.0)
        
    def test_update(self):
        self.CWP.damage_level = 0.3
        self.CWP_on_bridge.damage_level = 0.3
        self.CWP.update(self.dummy_sys)
        self.CWP_on_bridge.update(self.dummy_sys)
        self.assertEqual(self.CWP.functionality_level, 0.7)
        self.assertEqual(self.CWP_on_bridge.functionality_level, 0.7)
        self.assertEqual(self.CWP.supply['transfer_services'].initial['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.CWP_on_bridge.supply['transfer_services'].initial['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.CWP.supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.7)
        self.assertEqual(self.CWP_on_bridge.supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.7)
        self.assertEqual(self.CWP.demand['transfer_services'].current['BridgeTransferService'], 0.0)
        self.assertEqual(self.CWP_on_bridge.demand['transfer_services'].current['BridgeTransferService'], 1.0)
        
        self.CWP.damage_level = 1.0
        self.CWP_on_bridge.damage_level = 1.0
        self.CWP.update(self.dummy_sys)
        self.CWP_on_bridge.update(self.dummy_sys)
        self.assertEqual(self.CWP.functionality_level, 0.0)
        self.assertEqual(self.CWP_on_bridge.functionality_level, 0.0)
        self.assertEqual(self.CWP.supply['transfer_services'].initial['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.CWP_on_bridge.supply['transfer_services'].initial['CoolingWaterTransferService'], 0.8)
        self.assertEqual(self.CWP.supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.0)
        self.assertEqual(self.CWP_on_bridge.supply['transfer_services'].current['CoolingWaterTransferService'], 0.8*0.0)
        self.assertEqual(self.CWP.demand['transfer_services'].current['BridgeTransferService'], 0.0)
        self.assertEqual(self.CWP_on_bridge.demand['transfer_services'].current['BridgeTransferService'], 0.0)
        
        # test the case when the bridge that is carrying the links is not functional
                
class TestBridge(unittest.TestCase):
    
    def setUp(self):
        self.Bridge = Component.Bridge(1, 2)
        self.dummy_sys = System.System([], [])
        
    def test_constructor(self):
        self.assertEqual(self.Bridge.id, 21)
        self.assertEqual(self.Bridge.repair_rate, 0.01)
        self.assertEqual(self.Bridge.supply['transfer_services'].initial['BridgeTransferService'], 1.0)
        self.assertEqual(self.Bridge.demand['transfer_services'].initial['BridgeTransferService'], 0.0)
        
    def test_update(self):
        self.Bridge.damage_level = 0.05
        self.Bridge.update()
        self.assertEqual(self.Bridge.functionality_level, 0.0)
        self.assertEqual(self.Bridge.supply['transfer_services'].initial['BridgeTransferService'], 1.0)
        self.assertEqual(self.Bridge.supply['transfer_services'].current['BridgeTransferService'], 0.0)
        
        
if __name__ == '__main__':
    unittest.main()