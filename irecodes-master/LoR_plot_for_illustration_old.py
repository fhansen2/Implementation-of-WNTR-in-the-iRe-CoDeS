# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 12:37:38 2020

@author: nikola blagojevic e-mail: blagojevic@ibk.baug.ethz.ch
"""
import numpy as np
import plotly.graph_objects as go
import plotly.io as pio

### Creates an illustrative LoR Plot ###

# create dummy supply, demand and consumption values

# add 5 time steps before the disaster
warmup = 5

time_series = [-warmup, 0, 5, 10, 15, 20, 40, 60, 80, 100]

# one LoR plot to illustrate ReCoDeS
single_LoR_illustration_plot = True

# two LoR plot to illustrate the same LoR for different recovery
double_LoR_illustration_plot = True

if single_LoR_illustration_plot:
    total_supply = [100, 100, 20, 20, 40, 60, 80, 100, 100]
    total_demand = [80, 80, 40, 40, 40, 60, 60, 60, 80]
    total_consumption = [80, 80, 10, 10, 30, 40, 60, 60, 80]    

    rs_abbreviations = 'R/S'
    rs_units = ''
    legend_position = [0.99, 0.5]

    # Plotting using PLOTLY 
    # choose whether the plot should be shown in the browser or IDE
    pio.renderers.default = 'png'         
    # pio.renderers.default = 'browser'
    max_time_step = 100

    LoR_shade_color = 'rgba(0,191,255, 0.5)'                  
    fig = go.Figure()
    # independent values
    fig.add_trace(go.Scatter(x=time_series, y=total_demand, 
                name=r'$D_{sys, %s}$' % (rs_abbreviations), line_color = 'red')) 
    fig.add_trace(go.Scatter(x=time_series, y=total_supply,  
                name=r'$S_{sys, %s}^{C}$' % (rs_abbreviations), line_color = 'blue'))            
    fig.add_trace(go.Scatter(x=time_series, y=total_consumption, 
                name=r'$C_{sys, %s}$' % (rs_abbreviations), line_color = 'green'))            
    # add the shading between demand and consumption
    fig.add_trace(go.Scatter(x=np.concatenate([time_series[1:], time_series[1::-1]]), 
                                y=np.concatenate([total_demand[1:], total_consumption[::-1][1:]]), 
                name='LoRShade', fill='toself', hoveron=None,
                line_width=0, showlegend=False, mode='lines', line_color = LoR_shade_color))            


    fig.update_layout(xaxis_title = '$Time \space [day]$',
                    yaxis_title = '$Demand, \space Supply \space Capacity, \space Consumption \space$',
                    xaxis = dict(
                        linecolor = 'white',
                        linewidth = 2,
                        mirror = True),
                    yaxis = dict(
                        linecolor = 'white',
                        linewidth = 2,
                        mirror = True),                                                 
                        
                    legend = dict(                                  
                        x = legend_position[0],
                        y = legend_position[1],
                        yanchor = 'top',
                        xanchor = 'right',
                        bordercolor = 'Black',
                        borderwidth = 1),
                    paper_bgcolor="White",
                    autosize = False,
                    width = 700,
                    height = 500,                            
                    margin = dict(
                        l = 10,
                        r = 10,
                        b = 10,
                        t = 10,
                        pad = 4))

    fig.show()

if double_LoR_illustration_plot:
    total_supply_1 = [100, 100, 20, 20, 40, 90, 100, 100, 100]
    total_demand_1 = [90, 90, 60, 60, 60, 90, 90, 90, 90]
    total_consumption_1 = [90, 90, 0, 0, 0, 90, 90, 90, 90]    

    rs_abbreviations = 'R/S'
    rs_units = ''
    legend_position = [0.99, 0.5]

    # Plotting using PLOTLY 
    # choose whether the plot should be shown in the browser or IDE
    pio.renderers.default = 'png'         
    # pio.renderers.default = 'browser'
    max_time_step = 100

    LoR_shade_color = 'rgba(0,191,255, 0.5)'                  
    fig = go.Figure()
    # independent values
    fig.add_trace(go.Scatter(x=time_series, y=total_demand_1, 
                name=r'$D_{sys, %s}$' % (rs_abbreviations), line_color = 'red')) 
    fig.add_trace(go.Scatter(x=time_series, y=total_supply_1,  
                name=r'$S_{sys, %s}^{C}$' % (rs_abbreviations), line_color = 'blue'))            
    fig.add_trace(go.Scatter(x=time_series, y=total_consumption_1, 
                name=r'$C_{sys, %s}$' % (rs_abbreviations), line_color = 'green'))            
    # add the shading between demand and consumption
    fig.add_trace(go.Scatter(x=np.concatenate([time_series[1:], time_series[1::-1]]), 
                                y=np.concatenate([total_demand_1[1:], total_consumption_1[::-1][1:]]), 
                name='LoRShade', fill='toself', hoveron=None,
                line_width=0, showlegend=False, mode='lines', line_color = LoR_shade_color))            


    fig.update_layout(xaxis_title = '$Time \space [day]$',
                    yaxis_title = '$Demand, \space Supply \space Capacity, \space Consumption \space$',
                    xaxis = dict(
                        linecolor = 'white',
                        linewidth = 2,
                        mirror = True),
                    yaxis = dict(
                        linecolor = 'white',
                        linewidth = 2,
                        mirror = True),                                                 
                        
                    legend = dict(                                  
                        x = legend_position[0],
                        y = legend_position[1],
                        yanchor = 'top',
                        xanchor = 'right',
                        bordercolor = 'Black',
                        borderwidth = 1),
                    paper_bgcolor="White",
                    autosize = False,
                    width = 700,
                    height = 500,                            
                    margin = dict(
                        l = 10,
                        r = 10,
                        b = 10,
                        t = 10,
                        pad = 4))
    fig.show()
    save_name = 'LoR_plot_for_illustration_type_1'
    fig.savefig(save_name, dpi=150, bbox_inches = 'tight')

    total_supply_2 = [100, 100, 20, 20, 40, 90, 100, 100, 100]
    total_demand_2 = [90, 90, 80, 80, 80, 80, 80, 90, 90]
    total_consumption_2 = [90, 90, 65, 65, 65, 65, 65, 90, 90]    

    rs_abbreviations = 'R/S'
    rs_units = ''
    legend_position = [0.99, 0.5]

    # Plotting using PLOTLY 
    # choose whether the plot should be shown in the browser or IDE
    pio.renderers.default = 'png'         
    # pio.renderers.default = 'browser'
    max_time_step = 100

    LoR_shade_color = 'rgba(0,191,255, 0.5)'                  
    fig = go.Figure()
    # independent values
    fig.add_trace(go.Scatter(x=time_series, y=total_demand_1, 
                name=r'$D_{sys, %s}$' % (rs_abbreviations), line_color = 'red')) 
    fig.add_trace(go.Scatter(x=time_series, y=total_supply_1,  
                name=r'$S_{sys, %s}^{C}$' % (rs_abbreviations), line_color = 'blue'))            
    fig.add_trace(go.Scatter(x=time_series, y=total_consumption_1, 
                name=r'$C_{sys, %s}$' % (rs_abbreviations), line_color = 'green'))            
    # add the shading between demand and consumption
    fig.add_trace(go.Scatter(x=np.concatenate([time_series[1:], time_series[1::-1]]), 
                                y=np.concatenate([total_demand_1[1:], total_consumption_1[::-1][1:]]), 
                name='LoRShade', fill='toself', hoveron=None,
                line_width=0, showlegend=False, mode='lines', line_color = LoR_shade_color))            


    fig.update_layout(xaxis_title = '$Time \space [day]$',
                    yaxis_title = '$Demand, \space Supply \space Capacity, \space Consumption \space$',
                    xaxis = dict(
                        linecolor = 'white',
                        linewidth = 2,
                        mirror = True),
                    yaxis = dict(
                        linecolor = 'white',
                        linewidth = 2,
                        mirror = True),                                                 
                        
                    legend = dict(                                  
                        x = legend_position[0],
                        y = legend_position[1],
                        yanchor = 'top',
                        xanchor = 'right',
                        bordercolor = 'Black',
                        borderwidth = 1),
                    paper_bgcolor="White",
                    autosize = False,
                    width = 700,
                    height = 500,                            
                    margin = dict(
                        l = 10,
                        r = 10,
                        b = 10,
                        t = 10,
                        pad = 4))
    fig.show()
    save_name = 'LoR_plot_for_illustration_type_1'
    fig.savefig(save_name, dpi=150, bbox_inches = 'tight')