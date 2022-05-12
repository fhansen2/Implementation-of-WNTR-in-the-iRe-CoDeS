# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 13:35:01 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""

import Component
import numpy as np
from collections import defaultdict

# %% priorities class definition for each considered virtual community separately
class PrioritiesBaseClass():
    
    IDs = defaultdict(int) # make IDs a default dict that returns zero when there is a key error - make sure that no component has an ID of zero
    utilities = dict()
    
    # get the component ids of all components in the system 
    def get_component_ids(self, system):
        # this for loop can be more efficient if we do not loop over same components
        # consider implementing if this is slow
        for component in system.components:
            self.IDs[type(component).__name__] = component.id
            # TODO: Implement the ids for repair instances
            
    def get_sort_vector(self, system, rs_name):
        # add rs_group as the input when adding Impeding Factors and Recovery RSs
        current_priorities = np.asarray(self.utilities[rs_name])
        sorted_ids = np.zeros((len(system.components)))
        all_ids = []
        # collect component ids as ordered in the components property of the system
        # assumption: the system matrix will have components in the same order
        for component in system.components:
            all_ids.append(component.id)               

        first_el = 0
        for id in current_priorities:            
            temp = np.nonzero(all_ids == id)[0]      
            last_el = first_el + len(temp) - 1
            sorted_ids[first_el:last_el+1] = temp
            first_el = last_el + 1        
       
        return sorted_ids
    
    @staticmethod
    def remove_zero_ids(list):
       # removes zeros from a list - these are the ids of component that do not exist in the system
       filtered_list =  [i for i in list if i!=0]
       return filtered_list
    
# Priorities for the two component system (EPP and BSU) used for testing
class PrioritiesTwoCompSys(PrioritiesBaseClass):   
    
    
    # in this implementation, priorities are defined on a component type level
    # we prioritize certain component types over others
    # it can be changed to prioritize certain localities, certain damage levels etc.
    def set_EP_priority(self):
        # priorities according to the iReCoDeS paper 5-component example including links
        self.utilities['ElectricPower'] = self.remove_zero_ids([self.IDs['EPP'], self.IDs['BSU'], 
                                           self.IDs['Bridge'], self.IDs['EPTL'],
                                           self.IDs['CWP']])        
        
    def set_all_priorities(self, system):
        # call all methods that set priorities
        self.get_component_ids(system)
        self.set_EP_priority()         
              
            
# priorities for the five component system similar as the example in the iReCoDeS paper and used for testing here
class PrioritiesFiveCompSys(PrioritiesBaseClass):    

    
    # in this implementation, priorities are defined on a component type level
    # we prioritize certain component types over others
    # it can be changed to prioritize certain localities, certain damage levels etc.
    def set_EP_priority(self):
        
        self.utilities['ElectricPower'] = self.remove_zero_ids([self.IDs['EPP'], self.IDs['BTS'], 
                                self.IDs['CWF'], self.IDs['BSC'],
                                self.IDs['PWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
        
        
    def set_LLC_priority(self):
        
        self.utilities['LowLevelCommunication'] = self.remove_zero_ids([self.IDs['BTS'], self.IDs['BSC'], 
                                self.IDs['EPP'], self.IDs['CWF'],
                                self.IDs['PWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
        
    def set_CW_priority(self):
        
        self.utilities['CoolingWater'] = self.remove_zero_ids([self.IDs['CWF'], self.IDs['EPP'], 
                                self.IDs['BTS'], self.IDs['BSC'],
                                self.IDs['PWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
    
    # set dummy priorities for HighLevelCommunication and PotableWater - needed for interdependnecy modelling until I implement relevant faiclities
    def set_PW_priority(self):
        # priorities according to the iReCoDeS paper 5-component example
        self.utilities['PotableWater'] = self.remove_zero_ids([self.IDs['PWF'], self.IDs['EPP'], 
                                self.IDs['BTS'], self.IDs['BSC'],
                                self.IDs['CWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
        
    def set_HLC_priority(self):
        # priorities according to the iReCoDeS paper 5-component example
        self.utilities['HighLevelCommunication'] = self.remove_zero_ids([self.IDs['BSC'], self.IDs['BTS'], 
                                self.IDs['EPP'], self.IDs['CWF'],
                                self.IDs['PWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
        
        
    def set_all_priorities(self, system):
        # call all methods that set priorities
        self.get_component_ids(system)
        self.set_EP_priority()
        self.set_CW_priority()
        self.set_LLC_priority()
        self.set_PW_priority()
        self.set_HLC_priority()        
             

# %% define priorites for the virtual community
class PrioritiesVirtualCommunity(PrioritiesBaseClass):    
  
    
    # in this implementation, priorities are defined on a component type level
    # we prioritize certain component types over others
    # it can be changed to prioritize certain localities, certain damage levels etc.
    def set_EP_priority(self):
        # priorities according to the iReCoDeS paper 5-component example
        self.utilities['ElectricPower'] = self.remove_zero_ids([self.IDs['EPP'], self.IDs['BSC'], 
                                self.IDs['BTS'], self.IDs['CWF'],
                                self.IDs['PWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
    
        
    def set_HLC_priority(self):
        # priorities according to the iReCoDeS paper 5-component example
        self.utilities['HighLevelCommunication'] = self.remove_zero_ids([self.IDs['BSC'], self.IDs['BTS'], 
                                self.IDs['EPP'], self.IDs['CWF'],
                                self.IDs['PWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
        
    def set_LLC_priority(self):
        # priorities according to the iReCoDeS paper 5-component example
        self.utilities['LowLevelCommunication'] = self.remove_zero_ids([self.IDs['BTS'], self.IDs['EPP'], 
                                self.IDs['BSC'], self.IDs['CWF'],
                                self.IDs['PWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
        
    def set_CW_priority(self):
        # priorities according to the iReCoDeS paper 5-component example
        self.utilities['CoolingWater'] = self.remove_zero_ids([self.IDs['CWF'], self.IDs['PWF'], 
                                self.IDs['BTS'], self.IDs['EPP'],
                                self.IDs['BSC'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
    
    # set dummy priorities for HighLevelCommunication and PotableWater - needed for interdependnecy modelling until I implement relevant faiclities
    def set_PW_priority(self):
        # priorities according to the iReCoDeS paper 5-component example
        self.utilities['PotableWater'] = self.remove_zero_ids([self.IDs['PWF'], self.IDs['BTS'], 
                                self.IDs['EPP'], self.IDs['BSC'],
                                self.IDs['CWF'], self.IDs['BSU'],
                                self.IDs['Bridge'], self.IDs['EPTL'],
                                self.IDs['CWP'], self.IDs['PWP']])
        
        
    def set_all_priorities(self, system):
        # call all methods that set priorities
        self.get_component_ids(system)
        self.set_EP_priority()
        self.set_CW_priority()
        self.set_LLC_priority()
        self.set_PW_priority()
        self.set_HLC_priority()
        
          
    