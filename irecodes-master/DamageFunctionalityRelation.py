# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:31:44 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""

# %% DamageFunctionalityRelation classes - prepared for Strategy pattern

class linear: 
    
    def update(component):
    # round to 10 digits - if not it causes confussion later (e.g., 0.5 != 0.49999999999)
        component.functionality_level = round(1-component.damage_level, 5)

class binary: 
    
    def update(component):
        component.functionality_level = [0 if component.damage_level>0 else 1][0]
    
class step:
    
    def update(component):
        if component.damage_level > 0.3:
            component.functionality_level = 0.0
        else:
            component.functionality_level = 1.0    
    
