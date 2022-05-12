# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:31:10 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""
import numpy as np
import RSGroup
import DamageFunctionalityRelation
import math
import collections

# %% component class definition
class Component:   
    
    # constructor
    def __init__(self, start=None, end=None, bridge=False,
                 damage_functionality = DamageFunctionalityRelation.linear):
        self.damage_level = 0
        self.functionality_level = 1
        self.repair_rate = 0
        self.start_locality = start
        self.end_locality = end
        self.damage_functionality = damage_functionality
        # use dicts to store rsgroups - initialize dicts with rs group names
        self.supply = dict({'utilities': RSGroup.RSGroup(), 'transfer_services': RSGroup.RSGroup()})
        self.demand = dict({'utilities': RSGroup.RSGroup(), 'transfer_services': RSGroup.RSGroup()})
        self.id = None        
        
        # if the component is on a bridge, assign a demand for bridge services of 1 - this is the default value
        if bridge:
                demand_dict = RSGroup.OrderedDefaultDict([('BridgeTransferService', 1)])
                self.add_initial_demand_rs_group('transfer_services', demand_dict)
                # initiate the property that will store the reference to the bridge that is carrying the link
                self.bridge = None
     
    # damage setter    
    def set_damage(self, damage):
        self.damage_level = damage  
        
    # supply setter
    def add_initial_supply_rs_group(self, rs_group_name, rs_list):
        # if the rs group has not been created yet, create it now
        if not(rs_group_name in self.supply):
            self.supply[rs_group_name] = RSGroup.RSGroup()
        self.supply[rs_group_name].set_initial_rs_value(rs_list)
        
    # demand setter
    def add_initial_demand_rs_group(self, rs_group_name, rs_list):
        # if the rs group has not been created yet, create it now
        if not(rs_group_name in self.supply):
            self.supply[rs_group_name] = RSGroup.RSGroup()
        self.demand[rs_group_name].set_initial_rs_value(rs_list)
        
    # update functionality level - use Strategy pattern
    def update_func(self):
        self.damage_functionality.update(self)
     
    def update_supply(self):
        # update all rs groups
        for key in self.supply:
            self.supply[key].update(self.functionality_level)
        
    def update_demand(self, system=None):
        # assume demand is zero when 
        # the functionality level is zero
        # otherwise it is at its initial level
        # override in subclasses
        if self.functionality_level > 0:
            demand_level = 1
        else:
            demand_level = 0
        
        # update both the utilities and transfer service demand
        for key in self.demand:
            self.demand[key].update(demand_level)
        
    # updates the functionality level 
    # and supply and demand values 
    # based on the current damage level
    def update(self, system=None):
        self.update_func()
        self.update_supply()
        self.update_demand(system)
 
    # check whether all the demands are met for a component 
    def check_demand_indicators(self, matrix, comp_num, func_columns):
        return np.all(matrix[comp_num, func_columns] == 1)
                       
    # repair the component by decreasing its damage level by the repair rate
    # if the damage level goes below zero, set it to zero
    def repair(self):
        # round to prevent 0.5 != 0.499999999
        self.damage_level = round(self.damage_level - self.repair_rate, 5)
        if self.damage_level < 0:
            self.damage_level = 0
      
    # get the general properties of a component to fill out the first few columns of the system matrix
    def collect_general_properties(self, system):   
        # initialize the vector as an ordered dict - no problems with assuming vector length!
        general_properties = collections.OrderedDict()
        for key, value in system.system_matrix_col_ids.items():
            general_properties[value] = getattr(self, key)            
        # convert dict into a numpy array
        output = np.fromiter(general_properties.values(), dtype=float)        
        return output
        
    # collect the demand and supply values for the system matrix
    def collect_rs_demand_supply_values(self, rs_group_name, rs_names):
        # has to be reshaped to one dimensional np array
        rs_vector = np.reshape([self.demand[rs_group_name].get_rs_vector(rs_names), self.supply[rs_group_name].get_rs_vector(rs_names)], -1)
        return rs_vector

# %% define facilities and links - iReCoDeS paper (2020)

# %% class EPP - Electric Power Plant
class EPP(Component):    
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.linear):
        if start != end:
            print('ERROR: Start and end locality of an EPP must be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 1
            self.repair_rate = 0.01
            # values are from the iReCoDeS paper case study
            supply_dict = RSGroup.OrderedDefaultDict([('ElectricPower', 40)])
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPower', 0.2),
                                                      ('LowLevelCommunication', 0.001),
                                                      ('CoolingWater', 0.05)])
            self.add_initial_supply_rs_group('utilities', supply_dict)
            self.add_initial_demand_rs_group('utilities', demand_dict)
             # add the demand for transfer services  - the same amount as the demand
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPowerTransferService', 0.2),
                                                      ('CoolingWaterTransferService', 0.05)]) 
            self.add_initial_demand_rs_group('transfer_services', demand_dict)        
    
# %% class BSC - Base Station Controller
class BSC(Component):    
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.linear):
        if start != end:
            print('ERROR: Start and End locality of a BSC must be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 2
            self.repair_rate = 0.01
            # values are from the iReCoDeS paper case study
            supply_dict = RSGroup.OrderedDefaultDict([('HighLevelCommunication', 300)])
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPower', 0.2),
                                                      ('CoolingWater', 0.05)])                                                      
            self.add_initial_supply_rs_group('utilities', supply_dict)
            self.add_initial_demand_rs_group('utilities', demand_dict)
            # add the demand for transfer services  - the same amount as the demand
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPowerTransferService', 0.2),
                                                      ('CoolingWaterTransferService', 0.05)]) 
            self.add_initial_demand_rs_group('transfer_services', demand_dict)
       
    
# %% class BTS - Base Transceiver Station
class BTS(Component):    
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.binary):
        if start != end:
            print('ERROR: Start and End locality of a BTS must be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 3
            self.repair_rate = 0.05
            # values are from the iReCoDeS paper case study
            supply_dict = RSGroup.OrderedDefaultDict([('LowLevelCommunication', 45)])
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPower', 0.1),
                                                      ('HighLevelCommunication', 50)])                                                      
            self.add_initial_supply_rs_group('utilities', supply_dict)
            self.add_initial_demand_rs_group('utilities', demand_dict)
            
            # add the demand for transfer services  - the same amount as the demand
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPowerTransferService', 0.1)]) 
            self.add_initial_demand_rs_group('transfer_services', demand_dict)
 
# %% class PWF - Potable Water Facility
class PWF(Component):    
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.binary):
        if start != end:
            print('ERROR: Start and End locality of a PWF must be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 4
            self.repair_rate = 0.01
            # values are from the iReCoDeS paper case study
            supply_dict = RSGroup.OrderedDefaultDict([('PotableWater', 0.2)])
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPower', 0.1)])
            self.add_initial_supply_rs_group('utilities', supply_dict)
            self.add_initial_demand_rs_group('utilities', demand_dict)
            # add the demand for transfer services  - the same amount as the demand
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPowerTransferService', 0.1)]) 
            self.add_initial_demand_rs_group('transfer_services', demand_dict)
   
    
# %% class CWF - Cooling Water Facility
class CWF(Component):    
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.linear):
        if start != end:
            print('ERROR: Start and End locality of a CWF must be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 5
            self.repair_rate = 0.05
            # values are from the iReCoDeS paper case study
            supply_dict = RSGroup.OrderedDefaultDict([('CoolingWater', 0.06)])
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPower', 0.2),
                                                      ('LowLevelCommunication', 0.001)])                                                      
            self.add_initial_supply_rs_group('utilities', supply_dict)
            self.add_initial_demand_rs_group('utilities', demand_dict)
            # add the demand for transfer services  - the same amount as the demand
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPowerTransferService', 0.2)]) 
            self.add_initial_demand_rs_group('transfer_services', demand_dict)
               
    
# %% class BSU - Building Stock Unit 
class BSU(Component):
    
    # set the constant values for the post-disaster LowLevelCommunication change
    LLCMultiplier = 10
    ExpDecreaseFactor = -0.3        
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.linear):
        if start != end:
            print('ERROR: Start and end locality of a BSU must be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 6
            self.repair_rate = 0.01
            # demand values are from the small example in the iReCoDeS paper
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPower', 7.7),
                                                      ('LowLevelCommunication', 33.3),
                                                      ('PotableWater', 0.086)])
            
            self.add_initial_demand_rs_group('utilities', demand_dict)
            # add the demand for transfer services  - the same amount as the demand
            demand_dict = RSGroup.OrderedDefaultDict([('ElectricPowerTransferService', 7.7),
                                                      ('PotableWaterTransferService', 0.086)]) 
            self.add_initial_demand_rs_group('transfer_services', demand_dict)
    
    # override the parent method: change the demand for EP based on the functionality level
    # change the demand for LLC based on the amount of time from the disaster
    def update_demand(self, system):
        # get the current LLC demand 
        current_LLC_demand = self.demand['utilities'].current['LowLevelCommunication']
        
        # modify the LLC demand
        time_step = getattr(system, 'time_step')
        if time_step == 2 and self.damage_level > 0:
            # set the increased demand after the disaster
            self.demand['utilities'].current['LowLevelCommunication'] = current_LLC_demand * self.LLCMultiplier
        elif time_step > 2:
            # reduce the demand as the time goes by after the disaster
            self.demand['utilities'].current['LowLevelCommunication'] = current_LLC_demand * math.exp(self.ExpDecreaseFactor)
            # do not reduce the demand below the initial value
            if self.demand['utilities'].current['LowLevelCommunication'] < self.demand['utilities'].initial['LowLevelCommunication']:
                self.demand['utilities'].current['LowLevelCommunication'] = self.demand['utilities'].initial['LowLevelCommunication']    
                
        # modify the EP demand
        self.demand['utilities'].current['ElectricPower'] = self.demand['utilities'].initial['ElectricPower'] * self.functionality_level 
        self.demand['utilities'].current['PotableWater'] = self.demand['utilities'].initial['PotableWater'] * self.functionality_level 
        # consider implementing the observer pattern to match the transfer service demand to the utilities demand
        self.demand['transfer_services'].current['ElectricPowerTransferService'] = self.demand['transfer_services'].initial['ElectricPowerTransferService'] * self.functionality_level
        self.demand['transfer_services'].current['PotableWaterTransferService'] = self.demand['transfer_services'].initial['PotableWaterTransferService'] * self.functionality_level 
        
# %% class CWP - Cooling Water Pipe
class CWP(Component):
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.binary):
        if start == end:
            print('ERROR: Start and End Locality of a CWP must not be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 15
            self.repair_rate = 0.05            
            supply_dict = RSGroup.OrderedDefaultDict([('CoolingWaterTransferService', 0.8)])                                                                 
            self.add_initial_supply_rs_group('transfer_services', supply_dict)            
              
# %% class PWP - Potable Water Pipe
class PWP(Component):
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.binary):
        if start == end:
            print('ERROR: Start and End Locality of a CWP must not be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 14
            self.repair_rate = 0.05            
            supply_dict = RSGroup.OrderedDefaultDict([('PotableWaterTransferService', 0.8)])                                                                 
            self.add_initial_supply_rs_group('transfer_services', supply_dict)            
                      
    
# %% class EPTL - Electric Power Transmission Line
class EPTL(Component):
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.binary):
        if start == end:
            print('ERROR: Start and End Locality of an EPTL must not be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 11
            self.repair_rate = 0.05            
            supply_dict = RSGroup.OrderedDefaultDict([('ElectricPowerTransferService', 40)])                                                                 
            self.add_initial_supply_rs_group('transfer_services', supply_dict) 
                        

# %% class Bridge    
class Bridge(Component):
    
    def __init__(self, start, end, bridge = False,
                 damage_functionality = DamageFunctionalityRelation.binary):
        if start == end:
            print('ERROR: Start and End locality of a Bridge must not be the same')
        else:
            # initialize with the parent class method first, then add what you need
            super().__init__(start, end, bridge, damage_functionality)
            self.id = 21
            self.repair_rate = 0.01
            supply_dict = RSGroup.OrderedDefaultDict([('BridgeTransferService', 1)])
            self.add_initial_supply_rs_group('transfer_services', supply_dict)