# -*- coding: utf-8 -*-
"""
Created on Thu Oct  1 15:22:25 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""
import matplotlib.pyplot as plt
import numpy as np

# %% Class for visualising iRecodes results %% #
class Plotting():
    
    @staticmethod
    # create LoR plots for each utility
    def plot_LoR(system):
        rs_abbreviations = ['EP', 'HLC', 'LLC', 'PW', 'CW']
        rs_units_axis = ['MWh/day', 'E/day', 'E/day', 'Ml/day', 'Ml/day']
        rs_units_LoR = ['MWh', 'E', 'E', 'Ml', 'Ml']
        legend_position = [[0.97, 0.5], [0.97, 0.5], [0.97, 0.9], [0.97, 0.5], [0.97, 0.5]]
        LoR_values_position = [[0.97, 0.05], [0.97, 0.05], [0.97, 0.5], [0.97, 0.05], [0.97, 0.05]]
        for rs_id, rs_abbreviation in enumerate(rs_abbreviations): 
             Plotting.plot_LoR_single_diagram(system, rs_id, 
                                            rs_abbreviation, rs_units_axis[rs_id],                                                               
                                            rs_units_LoR[rs_id],
                                            LoR_values_position[rs_id],
                                            legend_position[rs_id])
    @staticmethod
    # create LoR plot of a single utility    
    def plot_LoR_single_diagram(system, rs_id, rs_abbreviation, rs_unit_axis, 
                                rs_unit_LoR, LoR_value_position, legend_position):     
               
        # get the data from the system
        supply = system.total_supply[:, rs_id]
        demand = system.total_demand[:, rs_id]
        consumption = system.total_consumption[:, rs_id]
        LoR_value = system.LoR[rs_id]
        # Plotting using MATPLOTLIB       
        plt.style.use('seaborn')          
        max_time_step = len(system.system_matrix)
        # add 5 time steps before the disaster
        warmup = 5
        time_series = np.arange(-warmup, max_time_step)
        LoR_shade_color = (0, 0.75, 1, 0.5)       
                 
        plt.Figure(figsize=(8, 6), dpi=150)
        # independent values
        total_supply_with_warmup = np.concatenate((np.repeat(supply[0], warmup), supply[:]), axis = 0)
        total_demand_with_warmup = np.concatenate((np.repeat(demand[0], warmup), demand[:]), axis = 0)
        total_consumption_with_warmup = np.concatenate((np.repeat(consumption[0], warmup), consumption[:]), axis = 0)
        plt.plot(time_series, total_demand_with_warmup, 
                 label=r'$D_{sys, %s}$' % (rs_abbreviation), color = 'red') 
        plt.plot(time_series, total_supply_with_warmup,  
                 label=r'$S_{sys, %s}^{C}$' % (rs_abbreviation), color = 'blue')            
        plt.plot(time_series, total_consumption_with_warmup, 
                 label=r'$C_{sys, %s}$' % (rs_abbreviation), color = 'green')          
        # add the shading between demand and consumption
        plt.fill_between(time_series, 
                         total_demand_with_warmup, 
                         total_consumption_with_warmup, 
                         label=r'$LoR_{sys, %s}$' % (rs_abbreviation),
                         color=LoR_shade_color, alpha=0.2)            
        # set the axis
        plt.xlabel(r'$Time \  [day]$')
        plt.ylabel(fr'$Demand,\  Supply\  Capacity,\  Consumption \  [{rs_unit_axis}]$')
        plt.xlim([-warmup, max_time_step-1])
        plt.ylim([0, max(1.2*max(total_demand_with_warmup), 1.2*max(total_supply_with_warmup))])
        # set the text box
        bbox_LoR = dict(boxstyle="square", facecolor=LoR_shade_color, edgecolor='black')    

        ax = plt.gca()
        plt.text(LoR_value_position[0], LoR_value_position[1], 
                 r'$LoR_{sys, %s} = %s %s $' % (rs_abbreviation, round(LoR_value, 2), rs_unit_LoR),                   
                 bbox=bbox_LoR, transform=ax.transAxes, 
                 horizontalalignment='right',
                 verticalalignment='bottom')              
        plt.legend(loc="upper right", 
                   bbox_to_anchor = (legend_position[0], legend_position[1]),                   
                   frameon=True, facecolor = 'white',
                   edgecolor = 'black')           
        plt.show()
        # save the figure
        savename = f'LoR_plot_{rs_abbreviation}.png'
        plt.savefig(savename, dpi=150) 
        plt.close()
  
    @staticmethod
    # create LoR plots for each utility for both independent and interdependent case
    def plot_dual_LoR(system_independent, system_interdependent):   
        # plt.style.use('seaborn')   
        plt.style.use('seaborn-paper')   
        

        rs_abbreviations = ['EP', 'HLC', 'LLC', 'PW', 'CW']
        rs_units_axis = ['MWh/day', 'E/day', 'E/day', 'Ml/day', 'Ml/day']
        rs_units_LoR = ['MWh', 'E', 'E', 'Ml', 'Ml']
        legend_position = [[0.97, 0.23], [0.97, 0.23], [0.97, 0.55], [0.97, 0.20], [0.97, 0.25]]
        LoR_values_position = [[0.97, 0.05], [0.97, 0.05], [0.97, 0.25], [0.97, 0.05], [0.97, 0.05]]
        # Plotting using matplotlib     
        max_time_step = len(system_independent.system_matrix)
        # add 5 time steps before the disaster
        warmup = 5
        time_series = np.arange(-warmup, max_time_step)
        LoR_shade_color_independent = (0.6, 0.8, 1)
        LoR_shade_color_interdependent = (0.7, 0.7, 0.7)
        # LoR_shade_color_independent = 'blue'
        # LoR_shade_color_interdependent = 'grey'
        # define which RSs to include in the plot - has to agree with rs_units and rs_abbreviations
        # TODO: fix later!
        rs_to_plot = [system_independent.considered_rs['utilities']]
        rs_to_plot = sum(rs_to_plot, [])
        
        for rs_id, utility in enumerate(rs_to_plot):            
            fig = plt.Figure(figsize=(11.69,8.27), dpi=300)
            plt.grid(True, color='black', linestyle= '-', linewidth = '0.1')
            # independent values
            total_supply_with_warmup = np.concatenate((np.repeat(system_independent.total_supply[0, rs_id], warmup), system_independent.total_supply[:, rs_id]), axis = 0)
            total_demand_with_warmup = np.concatenate((np.repeat(system_independent.total_demand[0, rs_id], warmup), system_independent.total_demand[:, rs_id]), axis = 0)
            total_consumption_with_warmup = np.concatenate((np.repeat(system_independent.total_consumption[0, rs_id], warmup), system_independent.total_consumption[:, rs_id]), axis = 0)
            # interdependent values
            total_supply_with_warmup_interdependent = np.concatenate((np.repeat(system_interdependent.total_supply[0, rs_id], warmup), system_interdependent.total_supply[:, rs_id]), axis = 0)
            total_demand_with_warmup_interdependent = np.concatenate((np.repeat(system_interdependent.total_demand[0, rs_id], warmup), system_interdependent.total_demand[:, rs_id]), axis = 0)
            total_consumption_with_warmup_interdependent = np.concatenate((np.repeat(system_interdependent.total_consumption[0, rs_id], warmup), system_interdependent.total_consumption[:, rs_id]), axis = 0)
            plt.plot(time_series, total_demand_with_warmup, 
                     label=r'$D_{sys, %s}$' % (rs_abbreviations[rs_id]), color = 'red')
            plt.plot(time_series, total_supply_with_warmup, '--',
                     label=r'$S_{sys, %s}^{C}$' % (rs_abbreviations[rs_id]), color = 'blue')          
            plt.plot(time_series, total_consumption_with_warmup, '--',
                     label=r'$C_{sys, %s}$' % (rs_abbreviations[rs_id]), color = 'green')
            plt.plot(time_series, total_supply_with_warmup_interdependent,  
                     label = r'$S_{sys, %s}^{C*}$' % (rs_abbreviations[rs_id]), color = 'blue')
            # fig.add_trace(go.Scatter(x=time_series, y=total_demand_with_warmup_interdependent, 
            #               name='Demand', line_color = 'red')) 
            plt.plot(time_series, total_consumption_with_warmup_interdependent, 
                     label=r'$C_{sys, %s}^{*}$' % (rs_abbreviations[rs_id]), color = 'green')
            # add the shading between demand and consumption
            plt.fill_between(time_series, 
                         total_demand_with_warmup, 
                         total_consumption_with_warmup,
                         label='_nolegend_',
                         # label=r'$LoR_{sys, %s}^{independent}$' % (rs_abbreviations[rs_id]), 
                         facecolor=LoR_shade_color_independent,
                         color=LoR_shade_color_independent, alpha=0.9)         
            plt.fill_between(time_series, 
                         total_demand_with_warmup_interdependent, 
                         total_consumption_with_warmup_interdependent, 
                         label='_nolegend_',
                         # label=r'$LoR_{sys, %s}^{interdependent}$' % (rs_abbreviations[rs_id]), 
                         facecolor=LoR_shade_color_interdependent,
                         color=LoR_shade_color_interdependent, alpha=0.5)   
             # set the axis
            plt.xlabel(r'$Time \  [day]$')
            plt.ylabel(fr'$Demand,\  Supply\  Capacity,\  Consumption \  [{rs_units_axis[rs_id]}]$')
            plt.xlim([-warmup, max_time_step-1])
            plt.ylim([0, max(1.2*max(total_demand_with_warmup), 1.2*max(total_supply_with_warmup))])
            # set the text box
            bbox_LoR_indep = dict(boxstyle="square", facecolor=LoR_shade_color_independent, edgecolor='black', alpha=0.7)    
            bbox_LoR_interdep = dict(boxstyle="square", facecolor=LoR_shade_color_interdependent, edgecolor='black', alpha=0.7)   
            ax = plt.gca()
            plt.text(LoR_values_position[rs_id][0], LoR_values_position[rs_id][1], 
                     r'$LoR_{sys, %s}^{*} = %s %s $' % (rs_abbreviations[rs_id], round(system_interdependent.LoR[rs_id], 2), rs_units_LoR[rs_id]),                   
                     bbox=bbox_LoR_interdep, transform=ax.transAxes, 
                     horizontalalignment='right',
                     verticalalignment='bottom')      
            plt.text(LoR_values_position[rs_id][0], LoR_values_position[rs_id][1] + 0.1, 
                     r'$LoR_{sys, %s} = %s %s $' % (rs_abbreviations[rs_id], round(system_independent.LoR[rs_id], 2), rs_units_LoR[rs_id]),                   
                     bbox=bbox_LoR_indep, transform=ax.transAxes, 
                     horizontalalignment='right',
                     verticalalignment='bottom')
            plt.legend(loc="lower right", 
                       bbox_to_anchor = (legend_position[rs_id][0], legend_position[rs_id][1]),                   
                       frameon=True, facecolor = 'white', framealpha=1.0,
                       edgecolor = 'black')     

            # make the background a bit darker
            # ax = plt.gca()
            # facecolor = ax.get_facecolor()      
            # new_facecolor = list(np.multiply(facecolor[:3],0.9))
            # new_facecolor.append(facecolor[3])
            # ax.set_facecolor(new_facecolor)
            # plt.show()
            # save the figure
            savename = f'LoR_plot_{rs_abbreviations[rs_id]}.png'
            plt.savefig(savename, dpi=300, bbox_inches='tight') 
            plt.close()        
       
    # plots the gant chart that illustrates who each component goes through recovery phases
    # such as impeding factors, repari and functionality, during community recovery
    def plot_gant_chart(self, system):        
        data = self.format_gant_data(system)
        # Make a dictionary of colors
        colors = {'Inspection': 'rgb(255, 0, 0)',
          'Design': 'rgb(0, 0, 255)',
          'Financing': 'rgb(0, 255, 0)',
          'Permitting': 'rgb(170, 14, 200)',
          'ContractorMobilization': 'rgb(14, 170, 200)',
          'Repair': 'rgb(170, 200, 14)',
          'Functional': 'rgb(170, 170, 200)'}
        fig = go.Figure()
        fig.update_xaxes(range=[0, system.time_step])
        
        y_labels = system.get_component_labels()
        for event in data.keys():  
            for i, component_data in enumerate(data[event]):
                if i == 0:
                    fig.add_trace(go.Bar(
                        y = [y_labels[i]],
                        x = component_data,
                        name = event, 
                        mode = 'markers',
                        marker = dict(symbol = 'square',
                                      color = colors[event], 
                                      size = 5)
                        ))
        fig.show()
        # save the figure
        pio.write_image(fig, 'GantChart.png', scale = 3)
    
    @staticmethod
    # format the system data to produce the gant chart using plotly
    def format_gant_data(system):
        # data need to be transformed into a list of dictionaries with keys
        # Task, Start and Finish
        # collect all events that should appear in the gant chart        
        # define data as a dictionary with data for each events
        data = {event: [] for event in system.considered_rs['impeding_factors']}
        data['Repair'] = []
        data['Functional'] = []       
        output = []
        component_labels = system.get_component_labels()
        for event in data.keys():            
            for i, component in enumerate(system.components):  
                # time steps in the data dictionary 
                # follow the same order of components in the system class
                time_steps = component.get_time_steps_field(event)  
                data[event].append(time_steps)              
                    
        return data
