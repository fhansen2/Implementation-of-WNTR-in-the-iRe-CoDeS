# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 12:15:42 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""

import collections
import copy

# %% add a defualt value to the ordered dict class - whenever the key does not exist return a zero
class OrderedDefaultDict(collections.OrderedDict):
    def __missing__(self, key):
        self[key] = 0.0
        # print('Key ' + str(key) + ' missing, returned 0')
        return 0.0
        
# %% rsgroup class definition - use ordered dicts to represent rs values
# RS == Resources or Services
class RSGroup():
    
    # constructor
    def __init__(self):
        # initialize all initial resource and service values as ordered dicts
        self.initial = OrderedDefaultDict()
        self.current = OrderedDefaultDict()             
    

    def set_initial_rs_value(self, rs_dict):  
        if type(rs_dict) == OrderedDefaultDict:
            # copy the input into class variables - make them deepcopies not references!
            self.initial = copy.deepcopy(rs_dict)
            self.current = copy.deepcopy(rs_dict)
        else:
            print('Input has to be an ordered dict!')
            
            
    # updates all the values in the rs group based on the functionality level
    def update(self, func_level):
        # go through all properties of the object
        for key in self.initial:
            self.current[key] = self.initial[key] * func_level

    # create a vector from rs group current properties to fill the matricies    
    def get_rs_vector(self, rs_names):
        # assemble the vector according to the order of names in rs names
        return [self.current[name] for name in rs_names]
    
    