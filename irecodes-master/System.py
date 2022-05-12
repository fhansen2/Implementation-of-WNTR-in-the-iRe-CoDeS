# -*- coding: utf-8 -*-
"""
Created on Tue Jun 23 17:31:44 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""

import numpy as np
import Component
import copy
import Priorities
import math
import itertools
import Plotting

# %% system class definition
class System:
    
    def __init__(self, considered_utilities, considered_transfer_services):
        # define resources and services considered by the system class
        self.considered_rs = dict()
        self.considered_rs['utilities'] = considered_utilities
        self.considered_rs['transfer_services'] = considered_transfer_services
        self.considered_utilities = considered_utilities
        self.considered_transfer_services = considered_transfer_services
        self.num_utilities = len(considered_utilities)
        self.num_transfer_services = len(considered_transfer_services)
        self.components = []
        self.time_step = 0
        # set the defualt value to 100, change if needed
        self.max_time_step = 1000
        # store system matrix at each time step
        self.system_matrix = dict()
        # decide on the organization of the first few columns in the system matrix
        self.system_matrix_col_ids = {'start_locality': 1,
                                      'end_locality': 2,
                                      'damage_level': 3,
                                      'functionality_level': 4,
                                      'id': 5}
        # this is the length of the general properties part of the System Matrix
        # modify when system_matrix_col_ids is changed
        self.system_matrix_offset = 5
        # define col ids of the matrix with demand values
        self.system_matrix_demand_col_ids = np.arange(self.system_matrix_offset, self.system_matrix_offset+self.num_utilities)
        # define col ids of the matrix with supply values
        self.system_matrix_supply_col_ids = np.arange(self.system_matrix_offset+self.num_utilities, self.system_matrix_offset+2*self.num_utilities)
        # define col ids of the matrix with demand met indicators
        self.system_matrix_demand_met_col_ids = np.arange(self.system_matrix_offset+2*self.num_utilities, self.system_matrix_offset+3*self.num_utilities)
        
        # set priorities
        # self.priorities = Priorities.Priorities()
        
        # initialize the variables to store total supply/demand/consumption values
        self.total_supply = np.empty((0, self.num_utilities))
        self.total_demand = np.empty((0, self.num_utilities))
        self.total_consumption = np.empty((0, self.num_utilities))               
        
        # initialize the transfer service supply matrix list - each element of the list
        # is the transfer supply matrix at that time step for each considered transfer service
        self.transfer_supply_matrix = [None for _ in range(self.max_time_step)] 
        # initialize the variable that stores all the potential paths between localities
        # this variables is assigned when the system is created, and it is used 
        # in the optimal path algorithm that selects the optimal path from this list
        # it is a dict of dicts
        # self.potential_paths = {key : dict() for key in self.considered_transfer_services}
        # variable that contains the links in paths
        self.potential_paths_links = {key : dict() for key in self.considered_transfer_services}
        
        # define which transfer service is needed for the transfer of which R/S
        # initialize with None values
        self.transfer_service_for_rs = {key: None for key in self.considered_utilities}
        self.transfer_service_for_rs['ElectricPower'] = 'ElectricPowerTransferService'
        self.transfer_service_for_rs['PotableWater'] = 'PotableWaterTransferService'
        self.transfer_service_for_rs['CoolingWater'] = 'CoolingWaterTransferService'
        # initialiaze the variable - choose whether the analysis is independent, interdependent or both
        self.consider_interdep = True
        
        self.num_rs_distributions = 0
        
    def __str__(self):
        # prints all the components in the order they are in the components property, and hence in the System matrix
        for i, component in enumerate(self.components):
            component_type = component.__class__.__name__
            damage = str(component.damage_level)
            print(f'{i}: Start: {component.start_locality} End: {component.end_locality} Component: {component_type} DamageLevel: {damage}')
    
    def get_component_labels(self):
        # returns a list of strings, where each string is the label of a component - needed for sobol analysis plots
        component_labels = []
        for component in self.components:
            component_type = component.__class__.__name__
            if component.start_locality == component.end_locality:
                # it is a facility, show only one locality
                component_label = component_type + ' ' + str(component.start_locality)
            else:
                component_label = component_type + ' (' + str(component.start_locality) + ', ' + str(component.end_locality) + ')'
            
            component_labels.append(component_label)
        
        return component_labels
                
                
    # method sets the potential paths variable 
    # @property
    def set_potential_paths(self, potential_paths):
        self.potential_paths = potential_paths         
        
    # create the system from the shape file
    def create_system(self, shape): 
        # reinitialize the components
        self.components = []
        # reset the created_link dict
        self.created_link = dict()
        # reset the create bridge list - this is not a dict, since we assume that a bridge 
        # is carrying all the links  - no separate bridge for each link  type
        self.created_bridge = np.empty((1, 2))
        # get the number of localities
        self.num_localities = len(shape)
        # get all combinations of localities without repeating the same ones
        self.localities_combination = [list(subset) for subset in itertools.combinations(range(1, self.num_localities+1), 2)]
        
        # shape file is defined as a list of dicts
        # go through all localities in the shape file and create components
        for locality in shape:
            self.create_facilities(locality)
            self.create_links(locality)         
           
            
    # create facilities
    def create_facilities(self, locality):    
        locality_id = locality['LocalityID']
        for key, value in locality['Content'].items():
            for comp in range(1, value+1):
                # get the class of the current facility based on the key
                current_comp = getattr(Component, key) 
                # create the component and add it to the system
                self.components.append(current_comp(start = locality_id,
                                                    end = locality_id))
                                                             
    # create links
    def create_links(self, locality):
        locality_id = locality['LocalityID']     
        # check if the locality has any links
        if 'LinkTo' in locality:
            # assume only one link of one link type can connect two localities        
            for key, value_list in locality['LinkTo'].items():
                for value in value_list:
                    # get the class of the current link
                    current_comp = getattr(Component, key)
                    # check if it already exists in the self.created_link dict
                    # first check if there is the key
                    if key in self.created_link:
                        link_exists = np.any(np.all(self.created_link[key] == [locality_id, value], axis=1))
                    else:
                        link_exists = False
                        
                    # if not, create the link
                    if not(link_exists):
                        # check whether the link is on a bridge
                        link_on_bridge = False
                        # get the end localities of the bridge from the BridgeTo key for the specific link  type
                        end_localities = locality.get('BridgeTo', dict()).get(key, [])                       
                        for end_locality in end_localities:
                            if end_locality == value:
                                 link_on_bridge = True
                                 # create the bridge only if it was not created earlier                              
                                 bridge_exists = np.any(np.all(self.created_bridge == [locality_id, value], axis=1))
                                 
                                 # if the bridge does not exist create it
                                 if not(bridge_exists):
                                     self.components.append(Component.Bridge(start = locality_id,
                                                                end = value)) 
                                     # store the current bridge - to link him to the corresponding link immediately
                                     current_bridge = self.components[-1]
                                     # update the self.created_bridge dict with the new bridge                                   
                                     self.created_bridge = np.vstack((self.created_bridge, np.asarray([[locality_id, value], [value, locality_id]])))
                                 else:
                                     # if the bridge already exists find it 
                                     # and set it as the current bridge, so you can connect it to the corresponding link
                                     for component in self.components:
                                         if (isinstance(component, Component.Bridge) and 
                                         (component.start_locality == locality_id or component.end_locality == locality_id) and
                                         (component.start_locality == end_locality or component.end_locality == end_locality)):
                                             current_bridge = component
                                             break
                                             
                                                                            
                        # create the link
                        self.components.append(current_comp(start = locality_id,
                                                            end = value, bridge = link_on_bridge))
                        # connect the link with the bridge that is carying the link when creating the link
                        if link_on_bridge:
                            current_link = self.components[-1]
                            current_link.bridge = current_bridge  
                                
                        # update the self.created_link dict with the new link
                        if key in self.created_link:
                            # if the key already exists append the new link to the links list
                            self.created_link[key] = np.vstack((self.created_link[key], np.asarray([[locality_id, value], [value, locality_id]])))
                        else:
                            # create the key if it does not exist
                            self.created_link[key] = np.asarray([[locality_id, value], [value, locality_id]])                                
                                                                             
    
    def set_priorities(self):
        # set priorities
        self.priorities.set_all_priorities(self)
        
    # set initial damage levels
    def set_damage(self, damage_vector):
        for i, component in enumerate(self.components):
            component.set_damage(damage_vector[i])
            
    # set repair rates from the vector - needed for the sobol analysis
    def set_repair_rates(self, repair_rate_vector):
        for i, component in enumerate(self.components):
            component.repair_rate = repair_rate_vector[i]
     
     # %% calculate LoR from the System Matricies
    # calculate total supply capacities of utilities at the current time step
    def get_supply_capacities(self):
        supply_capacities = np.sum(self.system_matrix[self.time_step][:, self.system_matrix_supply_col_ids], axis = 0)
        return(supply_capacities)
    
    # calculate total demand of utilities at the current time step
    # consider merging this and the get_supply_capacities method - they are almost identical
    def get_total_demand(self):
        total_demand = np.sum(self.system_matrix[self.time_step][:, self.system_matrix_demand_col_ids], axis = 0)
        return(total_demand)
    
    # calculate total consumption of utilities at the current time step
    # multiply the demands with the demand met columns from the system matrix
    def get_total_consumption(self):
        total_consumption = np.sum(np.multiply(self.system_matrix[self.time_step][:, self.system_matrix_demand_col_ids], 
                                               self.system_matrix[self.time_step][:, self.system_matrix_demand_met_col_ids]), axis = 0)
        return(total_consumption)
    
    # calculate the LoR for the entire recovery simulation
    def calculate_LoR(self):
        # for each system matrix from each time step get the total supply, demand, consumption vectors
        for time_step, _ in enumerate(self.system_matrix):
            # set the system time step - because methods that calcualte the supply/demand/consumption
            # take the system matrix from the current time step
            self.time_step = time_step
            self.total_supply = np.vstack((self.total_supply, self.get_supply_capacities()))
            self.total_demand = np.vstack((self.total_demand, self.get_total_demand()))
            self.total_consumption = np.vstack((self.total_consumption, self.get_total_consumption()))
        
        # calculate the LoR
        self.LoR = np.sum(self.total_demand-self.total_consumption, axis = 0)
        # self.LoR_norm = np.divide(self.LoR, np.sum(self.total_demand, axis = 0)) 
        # print(f'LoRs are: {str(self.LoR)}')
            
        
    # %% repair all components in a system   
    def repair(self):
        for component in self.components:
            component.repair()
            
    # %% update the functionality level and supply/demand values of components
    def update(self):
        for component in self.components:
            component.update(self)
   
    # %% method to assemble the system matrix
    def assemble_system_matrix(self):
        # get the max column id 
        max_col_id = max(self.system_matrix_col_ids.values()) + 4*len(self.considered_utilities)
        # assemble and store the matrix in self.system_matrix at each time step
        self.system_matrix[self.time_step] = np.zeros((len(self.components), max_col_id))
        # define columns of the matrix
        for row, component in enumerate(self.components):
            component_vector = [component.collect_general_properties(self), component.collect_rs_demand_supply_values('utilities', self.considered_utilities)]
            component_vector = np.reshape(np.concatenate(component_vector, axis = 0), (1, -1))
            self.system_matrix[self.time_step][row, :np.shape(component_vector)[1]] = component_vector
            # when assembling the system matrix set all demand met indicators to 1
            self.system_matrix[self.time_step][row, self.system_matrix_demand_met_col_ids] = 1
            
    # %% optimal path calculation methods    
        
    def create_potential_paths(self):
        # based on the potential_paths variables the algorithm finds the appropriate links 
        # that are used in the path, and creates a list of link component transfer service supply capacities
        # that is latter queried to find the optimal path form the list of potential paths
                
        # for each transfer service type
        for transfer_service, paths in self.potential_paths.items():
            # for each potential path for this transfer service
            for path, localities_list in paths.items(): 
                # initialize the list of links lists - each element of the list is one potential path
                self.potential_paths_links[transfer_service][path] = [] 
                # dissect the key to get the locality ids
                start, end = [int(locality) for locality in (path.split('from ')[1].split(' to '))]                        
                for localities in localities_list:
                    current_start = start
                    # initiate an empty list of links, fill it up with links of the path
                    self.potential_paths_links[transfer_service][path].append([])
                    # skip the first locality - the start locality
                    for locality in localities[1:]:
                        # find the link that connects the current start with the current locality and has a supply of the current transfer service
                        for component in self.components:
                            # assume all links can work both ways - from start to end and from end to start
                            if ((component.start_locality == current_start or component.start_locality == locality)
                                and (component.end_locality == locality or component.end_locality == current_start)
                                and component.supply['transfer_services'].initial[transfer_service] > 0):
                                self.potential_paths_links[transfer_service][path][-1].append(component)
                                # once you find it break the loop - assume that only one link of one type connects two localities
                                break
                        if locality == end:
                            # if the current locality is the end locality break the loop
                            break
                        else:
                            # if we did not reach the end locality, set the current locality as the start for the next link in the path
                            current_start = locality                                                                                  
                        
    def get_optimal_path(self, start, end, transfer_service):
        # Algorithm finds the optimal path between two localities from all the 
        # potential paths between the two localities
        # optimality is defined as maximizing the transfer service supply capacity
        # the transfer service supply of the path is the minimal transfer service supply
        # of all the links in the path
        # use the get methods to return None if the key does not exist
        potential_paths_links = self.potential_paths_links[transfer_service].get(f'from {int(start)} to {int(end)}', None)
        # if potential paths do not exist, return transfer suply of 0.0
        if potential_paths_links is None:
            optimal_transfer_supply = 0.0
            optimal_path = None
            return optimal_transfer_supply, optimal_path
        else:
            # if potential paths exist, find the optimal one
            # initialize the optimal path and optimal cost variables, if no paths exists, this is returned
            optimal_path = None
            optimal_transfer_supply = -math.inf
            # loop through all the paths and find the one with maximal minimal link transfer supply capacity
            for i, path in enumerate(potential_paths_links):
                # path transfer suply is the smallest transfer supply of all links in a path - if the list is empty return 0.0 transfer supply capacity
                path_transfer_supply = min([link.supply['transfer_services'].current[transfer_service] for link in path], default=0.0)
                # if the transfer supply of the current path is larger than optimal one,
                # current path becomes the optimal path
                if path_transfer_supply > optimal_transfer_supply:
                    optimal_transfer_supply = path_transfer_supply                
                    optimal_path = i
            
            return optimal_transfer_supply, optimal_path                            
    
    def get_path_functionality(self, start, end, transfer_service, transfer_service_demand):
        # method compares the transfer service demand and transfer service supply 
        # and calculates the path functionality          
        # here, path functionality is 1 if the transfer supply is larger than transfer demand
        # else path functionality is 0
        # if the transfer_service is None, the distributed R/S does not require any transfer service, so the path is always functional
        # also if the start is equal to the end locality
        if (transfer_service is None) or (start == end):
            path_functionality = 1
            return path_functionality
        else:
            optimal_transfer_supply, optimal_path = self.get_optimal_path(start, end, transfer_service)
            path_functionality = [1.0 if optimal_transfer_supply > transfer_service_demand else 0.0]
            return path_functionality[0]                                                                         

      
    # %% resource distribution method in the system class  
    
    # check whether the demand for bridge transfer services is met
    def distribute_bridge_transfer_service(self):
        for component in self.components:
            # check if the component is on a bridge
            if hasattr(component, 'bridge'):
                # if it does, it means that it is on a bridge
                # check whether the links is connected to the bridge that is carrying the link
                if not(component.bridge is None):
                    # check whether the demand for bridge services is met by the bridge
                    bridge_transfer_demand = component.demand['transfer_services'].current['BridgeTransferService']
                    bridge_transfer_supply = component.bridge.supply['transfer_services'].current['BridgeTransferService']
                    # if the bridge supply is not enough to meet the bridge demand, set the supply of the component to zero
                    if bridge_transfer_supply < bridge_transfer_demand:
                        update_level = 0
                        # update all rs groups
                        for key in component.supply:
                            component.supply[key].update(update_level)
                else:
                    print('ERROR: Link is not connected to the corresponding bridge')
                
    # resource distribution method vectorized
    def resource_distribution(self, rs_id, consider_interdep = False):
        matrix = self.system_matrix[self.time_step]
        # reorder rows according to component priorities 
        # assume rs_id is the position of the resource name in the considered utilities list
        sort_vector = self.priorities.get_sort_vector(self, self.considered_utilities[rs_id])
        
        # get the transfer service needed to trnasfer the current R/S
        current_transfer_service = self.transfer_service_for_rs[self.considered_utilities[rs_id]]
        
        # initialize suppliers: col 0: locality, col 1: supply capacity
        suppliers = suppliers_init = []
        # iterate through rows of the matrix - each row is one component
        for i in range(np.shape(matrix)[0]):
            component_row = int(sort_vector[i])
            component = matrix[component_row, :]
            # get the supply of the current component from the matrix    
            current_supply = component[self.system_matrix_supply_col_ids[rs_id]]
            
            if current_supply > 0:
                # add the current component to the list of suppliers
                suppliers.append([component[self.system_matrix_col_ids['start_locality']], current_supply])
                # if the current component is a supplier, put it on top of the suppliers list
                # it makes most sense that if the component is a supplier it should meet it's own demand first                
                suppliers[0], suppliers[1:] = suppliers[-1], suppliers[0:-1]
                component_is_supplier = True
            else:
                component_is_supplier = False
                
            # get the demand of the component
            current_demand = component[self.system_matrix_demand_col_ids[rs_id]]            
            
            if current_demand > 0:
                # save the suppliers in a separate variable - make a deepcopy not a reference
                # suppliers_init = copy.deepcopy(suppliers)
                # save the suppliers in a separate variable - avoid using deepcopy, takes too long
                suppliers_init = [i for i in suppliers]
                
                # get the demand amount and type of transfer service the component needs
                # if the current_transfer_service is None, the current R/S does not require a transfer service
                if not(current_transfer_service is None):                               
                    # assume that the order of components in the System matrix is the same as the order of components in the system                
                    transfer_service_demand = self.components[component_row].demand['transfer_services'].current[current_transfer_service]
                else:
                    transfer_service_demand = 0.0
                    
                # if there is demand, try to meet it using all the suppliers in the supplier list
                for supplier in suppliers:
                    
                    supplier_locality, current_supply = supplier                    
                    
                    path_func = self.get_path_functionality(supplier_locality, 
                                                            component[self.system_matrix_col_ids['start_locality']], 
                                                            current_transfer_service, 
                                                            transfer_service_demand)
                    
                    # increase the demand of the component to cover the transfer losses
                    if path_func > 0:
                        supply_needed = current_demand / path_func
                    else:
                        supply_needed = math.inf
                    
                    if supply_needed < current_supply:
                        # if the current supplier can meet the supply needed by the component
                        # set the current demand to zero, since it is met
                        # decrease the supply capacity of the supplier
                        supplier[1] = supplier[1] - supply_needed
                        current_demand = 0
                    else:
                        # if the current supplier cannot fully meet the demand of the user
                        # set its supply capacity to zero and take as much as he can give to the user
                        # but reduce it due to transfer losses
                        # check if the supplier can reach the component
                        if path_func > 0:
                            current_demand -= supplier[1] * path_func
                            supplier[1] = 0
                        
                    # after each supplier check if the demand is fully met
                    # break the loop if True, we do not need to go through the suppliers if the demand is met                    
                    if current_demand == 0:
                        break
                
                # if after trying to meet the demand with all suppliers
                # the demand is still not met, set the func indicator of the component to zero                              
                if current_demand > 0:
                    component[self.system_matrix_demand_met_col_ids[rs_id]] = 0
                    if consider_interdep:
                        # if we are considering interdependent effects, set the supply capacities to zero
                        component[self.system_matrix_supply_col_ids] = 0
                    
                    # since the demad is not met in full, reset the suppliers to their initial (unconsumed) values
                    suppliers = copy.deepcopy(suppliers_init)
            
            # if component was a supplier, reset the order of the suppliers list
            # put the current component at the bottom
            if component_is_supplier:
                suppliers[-1], suppliers[:-1] = suppliers[0], suppliers[1:]
                
            # fill the supply evolution columns here, if necessary            
                            
    # %% interdependency modelling in system class
    def interdependency_modelling(self, consider_interdep):
        
        # distribute resources following the RS distribution vector 
        # to simulate interdependency effects
        
        # first distribute non-interdependent RSs - here it is only the bridge transfer service
        self.distribute_bridge_transfer_service()
        
        # define the RS distribution sequence - all interdependent RSs appear once
        # assume only utilities are interdependent RSs
        rsds = np.arange(0, self.num_utilities)
        
        # define the RS distribution vector - repeat rsds as many time as there are interdependent RSs
        rsdv = np.tile(rsds, self.num_utilities)    
        
        # assemble the system matrix - a different one at each time step?
        self.assemble_system_matrix()        
        
        # initialize termination criteria
        stop = False
        # count iterations - for debugging purposes
        iter_num = 0
        while stop == False: 
            iter_num += 1            
                        
            supply_capacities = self.get_supply_capacities()
            
            for rs in rsdv:                                         
                
                # TODO: Implement relevant facilities                
                
                # distribute the rs - decide whether it is dependent or interdependnet based on the system variable 
                self.num_rs_distributions += 1
                self.resource_distribution(rs, consider_interdep)
                
            supply_capacities_modified = self.get_supply_capacities()
            
            # stop is True if supply capacities are the same (but rounded!) - breaks the loop
            stop = np.all(np.round(supply_capacities, 10) == np.round(supply_capacities_modified, 10))
    
    # method implements the recovery target, and checks whether it is met at the current time step
    # current recovery target is that the damage level of all components is zero
    def check_recovery_target(self):
        return np.all([round(component.damage_level, 5) == 0 for component in self.components])      
                                   
            
    # %% recovery simulation in system class
    def recovery_simulation(self, damage_vector, consider_interdep = True, plot_LoR = True): 
        # set all priorities
        self.priorities.set_all_priorities(self)    
        # define potential paths
        self.create_potential_paths()
        # choose whether the analysis is independent or interdependent
        self.consider_interdep = consider_interdep  
        
        stop = False
        # start the simulation
        for time_step in range(self.max_time_step):
            
            # check if the recovery target is met: check_recovery_target returns False when the target is not met            
            if self.check_recovery_target() and time_step > 1:
                stop = True
            
            # print(f'Time step: {str(time_step)}')
            self.time_step = time_step
            
            # assign damage time_step 1, time step zero is the pre-disaster state
            if time_step == 1:
                self.set_damage(damage_vector)
            
            # update the functionality and supply/demand values of components
            self.update()                       
            
            # distribute R/Ss and simulate interdependency effects
            self.interdependency_modelling(consider_interdep)
            
            # repair the components after time_step 1
            if time_step > 1:
                self.repair()  
            
         
            # do not break immediately after it is recovered to have 
            # a post disaster step where the system is fully recovered
            if stop:
                break
                   
        print(f'Total num of R/S distributions: {self.num_rs_distributions}')
        self.calculate_LoR()    
        
        if plot_LoR:
            Plotting.Plotting.plot_LoR(self) 

            
# =============================================================================
#     # create LoR plots for each utility    
#     def plot_LoR(self):       
#         rs_abbreviations = ['EP', 'HLC', 'LLC', 'PW', 'CW']
#         rs_units = ['MWh', 'E', 'E', 'Ml/day', 'Ml/day']
#         legend_position = [[0.99, 0.5], [0.99, 0.5], [0.99, 0.99], [0.99, 0.5], [0.99, 0.5]]
#         LoR_values_position = [[0.99, 0.05], [0.99, 0.05], [0.99, 0.5], [0.99, 0.05], [0.99, 0.05]]
#         
#         # Plotting using PLOTLY 
#         # choose whether the plot should be shown in the browser or IDE
#         pio.renderers.default = 'png'         
#         # pio.renderers.default = 'browser'
#         max_time_step = len(self.system_matrix)
#         # add 5 time steps before the disaster
#         warmup = 5
#         time_series = np.arange(-warmup, max_time_step)
#         LoR_shade_color = 'rgba(0,191,255, 0.5)'        
#         for rs_id, utility in enumerate(self.considered_utilities):            
#             fig = go.Figure()
#             # independent values
#             total_supply_with_warmup = np.concatenate((np.repeat(self.total_supply[0, rs_id], warmup), self.total_supply[:, rs_id]), axis = 0)
#             total_demand_with_warmup = np.concatenate((np.repeat(self.total_demand[0, rs_id], warmup), self.total_demand[:, rs_id]), axis = 0)
#             total_consumption_with_warmup = np.concatenate((np.repeat(self.total_consumption[0, rs_id], warmup), self.total_consumption[:, rs_id]), axis = 0)
#             fig.add_trace(go.Scatter(x=time_series, y=total_demand_with_warmup, 
#                           name=r'$D_{sys, %s}$' % (rs_abbreviations[rs_id]), line_color = 'red')) 
#             fig.add_trace(go.Scatter(x=time_series, y=total_supply_with_warmup,  
#                           name=r'$S_{sys, %s}^{C}$' % (rs_abbreviations[rs_id]), line_color = 'blue'))            
#             fig.add_trace(go.Scatter(x=time_series, y=total_consumption_with_warmup, 
#                           name=r'$C_{sys, %s}$' % (rs_abbreviations[rs_id]), line_color = 'green'))            
#             # add the shading between demand and consumption
#             fig.add_trace(go.Scatter(x=np.concatenate([time_series, time_series[::-1]]), 
#                                         y=np.concatenate([total_demand_with_warmup, total_consumption_with_warmup[::-1]]), 
#                           name='LoRShade', fill='toself', hoveron=None,
#                           line_width=0, showlegend=False, mode='lines', line_color = LoR_shade_color))            
#             
#             
#             fig.update_layout(xaxis_title = '$Time \space [day]$',
#                               yaxis_title = f'$Demand, \space Supply \space Capacity, \space Consumption \space [{rs_units[rs_id]}]$',
#                               xaxis = dict(
#                                   linecolor = 'white',
#                                   linewidth = 2,
#                                   mirror = True),
#                               yaxis = dict(
#                                   linecolor = 'white',
#                                   linewidth = 2,
#                                   mirror = True),
#                               annotations = [                                  
#                                   go.layout.Annotation( x = LoR_values_position[rs_id][0],
#                                            y = LoR_values_position[rs_id][1] + 0.07,
#                                            align = 'right',
#                                            text = r'$LoR_{sys, %s} = %s %s $' % (rs_abbreviations[rs_id], round(self.LoR[rs_id], 2), rs_units[rs_id]),
#                                            showarrow = False,
#                                            xref = 'paper',
#                                            yref = 'paper',
#                                            bordercolor = 'black',
#                                            borderpad = 4,
#                                            bgcolor = LoR_shade_color)],
#                               legend = dict(                                  
#                                   x = legend_position[rs_id][0],
#                                   y = legend_position[rs_id][1],
#                                   yanchor = 'top',
#                                   xanchor = 'right',
#                                   bordercolor = 'Black',
#                                   borderwidth = 1),
#                               paper_bgcolor="White",
#                               autosize = False,
#                               width = 700,
#                               height = 500,                            
#                               margin = dict(
#                                   l = 10,
#                                   r = 10,
#                                   b = 10,
#                                   t = 10,
#                                   pad = 4))
#             
#             fig.show()
# =============================================================================
    
    # create LoR plots for each utility for both independent and interdependent case
# =============================================================================
#     def plot_dual_LoR(self, system_interdependent):       
#         rs_abbreviations = ['EP', 'HLC', 'LLC', 'PW', 'CW']
#         rs_units = ['MWh', 'E', 'E', 'Ml/day', 'Ml/day']
#         legend_position = [[0.99, 0.5], [0.99, 0.5], [0.99, 0.99], [0.99, 0.5], [0.99, 0.5]]
#         LoR_values_position = [[0.99, 0.05], [0.99, 0.05], [0.99, 0.5], [0.99, 0.05], [0.99, 0.05]]
#         
#         # Plotting using PLOTLY 
#         # choose whether the plot should be shown in the browser or IDE
#         pio.renderers.default = 'png'         
#         # pio.renderers.default = 'browser'
#         max_time_step = len(self.system_matrix)
#         # add 5 time steps before the disaster
#         warmup = 5
#         time_series = np.arange(-warmup, max_time_step)
#         LoR_shade_color_independent = 'rgba(0,191,255, 0.5)'
#         LoR_shade_color_interdependent = 'rgba(255,250,250, 0.5)'
#         for rs_id, utility in enumerate(self.considered_utilities):            
#             fig = go.Figure()
#             # independent values
#             total_supply_with_warmup = np.concatenate((np.repeat(self.total_supply[0, rs_id], warmup), self.total_supply[:, rs_id]), axis = 0)
#             total_demand_with_warmup = np.concatenate((np.repeat(self.total_demand[0, rs_id], warmup), self.total_demand[:, rs_id]), axis = 0)
#             total_consumption_with_warmup = np.concatenate((np.repeat(self.total_consumption[0, rs_id], warmup), self.total_consumption[:, rs_id]), axis = 0)
#             # interdependent values
#             total_supply_with_warmup_interdependent = np.concatenate((np.repeat(system_interdependent.total_supply[0, rs_id], warmup), system_interdependent.total_supply[:, rs_id]), axis = 0)
#             total_demand_with_warmup_interdependent = np.concatenate((np.repeat(system_interdependent.total_demand[0, rs_id], warmup), system_interdependent.total_demand[:, rs_id]), axis = 0)
#             total_consumption_with_warmup_interdependent = np.concatenate((np.repeat(system_interdependent.total_consumption[0, rs_id], warmup), system_interdependent.total_consumption[:, rs_id]), axis = 0)
#             fig.add_trace(go.Scatter(x=time_series, y=total_demand_with_warmup, 
#                           name=r'$D_{sys, %s}$' % (rs_abbreviations[rs_id]), line_color = 'red')) 
#             fig.add_trace(go.Scatter(x=time_series, y=total_supply_with_warmup,  
#                           name=r'$S_{sys, %s}^{C, independent}$' % (rs_abbreviations[rs_id]), line_color = 'blue', line_dash = 'dash'))            
#             fig.add_trace(go.Scatter(x=time_series, y=total_consumption_with_warmup, 
#                           name=r'$C_{sys, %s}^{independent}$' % (rs_abbreviations[rs_id]), line_color = 'green', line_dash = 'dash'))
#             fig.add_trace(go.Scatter(x=time_series, y=total_supply_with_warmup_interdependent,  
#                           name= r'$S_{sys, %s}^{C, interdependent}$' % (rs_abbreviations[rs_id]), line_color = 'blue')) 
#             # fig.add_trace(go.Scatter(x=time_series, y=total_demand_with_warmup_interdependent, 
#             #               name='Demand', line_color = 'red')) 
#             fig.add_trace(go.Scatter(x=time_series, y=total_consumption_with_warmup_interdependent, 
#                           name=r'$C_{sys, %s}^{interdependent}$' % (rs_abbreviations[rs_id]), line_color = 'green'))
#             # add the shading between demand and consumption
#             fig.add_trace(go.Scatter(x=np.concatenate([time_series, time_series[::-1]]), 
#                                         y=np.concatenate([total_demand_with_warmup, total_consumption_with_warmup[::-1]]), 
#                           name='LoRShade', fill='toself', hoveron=None,
#                           line_width=0, showlegend=False, mode='lines', line_color = LoR_shade_color_independent))
#             
#             fig.add_trace(go.Scatter(x=np.concatenate([time_series, time_series[::-1]]), 
#                                         y=np.concatenate([total_demand_with_warmup_interdependent, total_consumption_with_warmup_interdependent[::-1]]), 
#                           name='LoRShade', fill='toself', hoveron=None,
#                           line_width=0, showlegend=False, mode='lines', line_color = LoR_shade_color_interdependent))
#             
#             fig.update_layout(xaxis_title = '$Time \space [day]$',
#                               yaxis_title = f'$Demand, \space Supply \space Capacity, \space Consumption \space [{rs_units[rs_id]}]$',
#                               xaxis = dict(
#                                   linecolor = 'white',
#                                   linewidth = 2,
#                                   mirror = True),
#                               yaxis = dict(
#                                   linecolor = 'white',
#                                   linewidth = 2,
#                                   mirror = True),
#                               annotations = [
#                                   go.layout.Annotation( x = LoR_values_position[rs_id][0],
#                                        y = LoR_values_position[rs_id][1],
#                                        align = 'right',
#                                        text = r'$LoR_{sys, %s}^{interdependent} = %s %s $' % (rs_abbreviations[rs_id], round(system_interdependent.LoR[rs_id], 2), rs_units[rs_id]),
#                                        showarrow = False,
#                                        xref = 'paper',
#                                        yref = 'paper',
#                                        bordercolor = 'black',
#                                        borderpad = 4,
#                                        bgcolor = LoR_shade_color_interdependent),
#                                   go.layout.Annotation( x = LoR_values_position[rs_id][0],
#                                            y = LoR_values_position[rs_id][1] + 0.07,
#                                            align = 'right',
#                                            text = r'$LoR_{sys, %s}^{independent} = %s %s $' % (rs_abbreviations[rs_id], round(self.LoR[rs_id], 2), rs_units[rs_id]),
#                                            showarrow = False,
#                                            xref = 'paper',
#                                            yref = 'paper',
#                                            bordercolor = 'black',
#                                            borderpad = 4,
#                                            bgcolor = LoR_shade_color_independent)],
#                               legend = dict(                                  
#                                   x = legend_position[rs_id][0],
#                                   y = legend_position[rs_id][1],
#                                   yanchor = 'top',
#                                   xanchor = 'right',
#                                   bordercolor = 'Black',
#                                   borderwidth = 1),
#                               paper_bgcolor="White",
#                               autosize = False,
#                               width = 700,
#                               height = 500,                            
#                               margin = dict(
#                                   l = 10,
#                                   r = 10,
#                                   b = 10,
#                                   t = 10,
#                                   pad = 4))
#             
#             fig.show()
#             # save the figure
#             pio.write_image(fig, f'LoR_plot_{rs_abbreviations[rs_id]}.png', scale = 3)
# =============================================================================
            
# %% methods not used at the moment
# =============================================================================
#     def find_optimal_paths(self):
#         # initialize check dict
#         check = {key: True for key in self.considered_transfer_services}        
#         # find an optimal path for each path defined in localities combinations        
#         for path in self.localities_combination:
#             # get the start and end locality id
#             start = path[0]
#             end = path[1]
#             # path for each considered transfer service
#             for transfer_service in self.considered_transfer_services:
#                 # consider not calculating paths for a transfer service
#                 # if the transfer supply matricies did not change compared to the 
#                 # previous time step                
#                 if self.time_step >= 1:
#                     check[transfer_service] = not(np.array_equal(
#                         self.transfer_supply_matrix[self.time_step-1][transfer_service],
#                         self.transfer_supply_matrix[self.time_step][transfer_service]))
#                     # if the transfer supply matricies are the same, the optimal paths will be the same
#                     self.optimal_paths[self.time_step][transfer_service] = copy.deepcopy(self.optimal_paths[self.time_step-1][transfer_service])
#                     break
#                 else:
#                     # but always calculate paths at the first time step
#                     check[transfer_service] = True
#                     
#                 # calculate optimal paths only when needed - saves computational time
#                 if check[transfer_service]:
#                     path_transfer_capacity, path_links = self.lca(start, end, transfer_service)
#                     # if the key of the dict has not been initialized, intialize it
#                     if not(self.optimal_paths[self.time_step][transfer_service]):
#                         self.optimal_paths[self.time_step][transfer_service] = np.zeros((self.num_localities, self.num_localities))                                  
#                     
#                     # fill the optimal path matrix symettrically
#                     self.optimal_paths[self.time_step][transfer_service][start, end] = path_transfer_capacity
#                     self.optimal_paths[self.time_step][transfer_service][end, start] = path_transfer_capacity    
# =============================================================================                                

# =============================================================================
#     def lca(self, start, end, transfer_service):    
#     # NOT TESTED
#     # Algorithm is not used - not suitable for current implementation of links
#     # since there is no cumulative path cost, the path cost at this moment (July2020)
#     # However, it will be needed for optimal path for ROADS
#     # is the minimal transfer service supply capacity of all links in the path
#     # [optCost, optPath] = lca(A,startNode,terminalNode)
#     #
#     # Executes Label Correcting algorithm (Book Dynamic Programming and Optimal
#     # Control, Bertsekes, page 81) using the depth-first method.
#     #
#     # Input:
#     #   A               [NxN] matrix, where the element A(i,j) = a_ij is the cost
#     #                   to move from node i to j.
#     #   startNode       Start node of desired shortest path, scalar from 1 to N.
#     #   terminalNode    Terminal node of desired shortest path, scalar from 1
#     #                   to N.
#     #
#     # Output:
#     #   optCost         Cost of the shortest path(s), scalar:
#     #   optPath         Row vector containing the shortest path, e.g. 
#     #                   optPath = [1 33 45 43 79 100].
#     
#         ### Initialize        
#         # Dimension of the problem: N = total number of nodes
#         N = self.num_localities 
#         
#         # Vector holding label d for each locality. 
#         # d[i] represents the shortest path found so far
#         d = np.full(N, math.inf) 
#         d[start-1] = 0.0
#         # Vector containing the parent of the shortest path found so far for each locality
#         parent = np.full(N, math.inf)
#         parent[start-1] = 0.0
#         # List containing all the localities that are currently active - candidates list
#         OPEN = np.zeros(N, dtype=int)
#         # pointer that points to the last element in OPEN
#         pointerOPEN = 0
#         OPEN[pointerOPEN] = start
#         
#         # label dt, represents the shortest path found so far
#         UPPER = math.inf
#         
#         # get the cost matrix - negative value of the transfer supply matrix at the current time step
#         # values have to be negative because we need the path with MAXIMAL supply capacity
#         # and LCA find the path with MINIMAL cost
#         cost_matrix = np.multiply(self.transfer_supply_matrix[self.time_step][transfer_service], -1)
#         # and zero supply capacity becomes infinite cost
#         cost_matrix[cost_matrix == 0.0] = math.inf
#         # infinite supply capacity becomes 0 cost
#         cost_matrix[cost_matrix == -math.inf] = 0.0        
#               
# 
#         # Check start and end nodes
#         if start == end:
#             optCost = math.inf
#             optPath = [start, end]            
#             return optCost, optPath
#         
#         if start > N or end > N:
#             optCost = 0.0
#             optPath = [start, end]
#             return optCost, optPath
#         
#         # Execute Label Correcting Algorithm        
#         while True:
#             # STEP 1: Remove locality i from OPEN and for each child j of i, execute STEP 2            
#             i = OPEN[pointerOPEN]
#             OPEN[pointerOPEN] = 0
#             pointerOPEN -= 1
#             
#             # find children of the current parent - those localities to which the cost is not inf            
#             children = np.where(cost_matrix[int(i-1), :] != math.inf)[0] + 1
#             # remove the current parent from the list
#             children = children[children != i]          
#                         
#             for child in children:
#                 # STEP 2: If d_i + a_ij < min(d_j, UPPER), set d_child = d_i + a_i, child
#                 # and set i to be the parent of child                
#                 if d[i-1] + cost_matrix[i-1, child-1] < min(d[child-1], UPPER):
#                     d[child-1] = d[i-1] + cost_matrix[i-1, child-1]
#                     parent[child-1] = i               
#                     
#                     # In addition, if child!=end, place child in OPEN if it is not already
#                     # in OPEN, while if child==end, set UPPER to the new value d_i + a_it of d_t (modification: UPPER is only the transfer supply)
#                     if child != end:
#                         if not((OPEN == child).any()):
#                             pointerOPEN = pointerOPEN + 1
#                             OPEN[pointerOPEN] = child
#                     else:
#                         UPPER = d[child-1]
#                             
#             # STEP 3: if OPEN is empty (pointerOPEN=-1), terminate: else go to STEP 1
#             # check this
#             if pointerOPEN == -1:
#                 break
#         
#         # DONE
#         # UPPER is equal to the cost of the shortest path
#         # but this is only the last cost - not the minimal cost of all costs!!!
#         optCost = UPPER
#   
#         
#         # Construct shortest path
#         # Start at end and for each node, take its parent node until we find ourselves at the start node
#         optPath = [end]
#         if parent[optPath[-1]-1] == math.inf:
#             optPath = 0
#         else:
#             while optPath[-1] != start:                
#                 optPath.append(int(parent[optPath[-1]-1]))                
#                 
#      
#         optPath.reverse()                                       
#         
#         return optCost, optPath
# =============================================================================

# =============================================================================
# # create the path cost matrix that serves as the input for the LCA optimal path algorithms                
#     def assemble_transfer_supply_matrix(self):
#         # a dict of [N x N] matricies, wehre the element A[i, j] is the transfer service supply capacity to move from locality i to locality j
#         # each transfer service gets a separate matrix - initialize the matrix with 0
#         transfer_supply_matrix = {key: np.full((self.num_localities, self.num_localities), 0.0) for key in self.considered_transfer_services}
#         # diagonal elements are infinite - transfer inside a locality unconstrained
#         for key, value in transfer_supply_matrix.items():
#             np.fill_diagonal(value, math.inf)
#         
#         # go through all components 
#         for component in self.components:
#             # get the transfer service only from links
#             if component.start_locality != component.end_locality:
#                 for transfer_service in self.considered_transfer_services:
#                     transfer_supply = component.supply['transfer_services'].current[transfer_service]                
#                     # decrease the locality by 1 - locality IDs start from 1 and matrix indices from 0
#                     start = component.start_locality-1
#                     end = component.end_locality-1
#                     transfer_supply_matrix[transfer_service][start, end] += transfer_supply
#                     # assume matrix is symmetric
#                     transfer_supply_matrix[transfer_service][end, start] += transfer_supply                
#         
#         self.transfer_supply_matrix[self.time_step] = transfer_supply_matrix        
# =============================================================================
    