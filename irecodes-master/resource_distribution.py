
import copy
import itertools
import math

import numpy as np
import wntr

import Component
import Plotting
import Priorities


class System:

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
                            
