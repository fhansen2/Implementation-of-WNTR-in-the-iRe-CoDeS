import numpy as np
import matplotlib.pyplot as plt

# create an illustration of the LoR plot for the iRecodes paper
create_dummy_LoR_plot = True
if create_dummy_LoR_plot:
    supply = np.asarray([100, 20, 20, 50, 50, 50, 50, 70, 70, 100, 100])
    demand = np.asarray([90, 65, 65, 65, 65, 65, 75, 75, 85, 90, 90])
    consumption = np.asarray([90, 10, 10, 30, 35, 35, 40, 40, 60, 90, 90])
    max_time_step = len(supply)
    time_series = np.arange(max_time_step)
    rs_abbreviation = 'R/S'
    legend_position = [0.97, 0.3]
    # Plotting using MATPLOTLIB       
    plt.style.use('seaborn')      

    # add 1 time steps before the disaster
    warmup = 1
    time_series = np.arange(-warmup, max_time_step)
    LoR_shade_color = (0, 0.75, 1, 0.5)       
                
    plt.Figure(figsize=(8, 6), dpi=150)
    # independent values
    total_supply_with_warmup = np.concatenate((np.repeat(supply[0], warmup), supply[:]), axis = 0)
    total_demand_with_warmup = np.concatenate((np.repeat(demand[0], warmup), demand[:]), axis = 0)
    total_consumption_with_warmup = np.concatenate((np.repeat(consumption[0], warmup), consumption[:]), axis = 0)

    # %% Plot only the supply first
    plt.plot(time_series, total_supply_with_warmup,  
                label=r'$S_{sys, %s}^{C}$' % (rs_abbreviation), color = 'blue')   

    # %% set the figure layout          
    # set the axis
    plt.xlabel(r'$Time \ Step$')
    plt.ylabel(r'$Demand,\  Supply\  Capacity,\  Consumption$')
    plt.xlim([-warmup, max_time_step-1])
    ticks = [0 ,2, 4, 6, 8, 10]
    labels = [r'$0 = t_{0}$', '2', '4', '6', '8', r'$10 = t_{f}$']
    ax = plt.gca()
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    plt.ylim([0, max(1.2*max(total_demand_with_warmup), 1.2*max(total_supply_with_warmup))])
    # set the text box
    bbox_LoR = dict(boxstyle="square", facecolor=LoR_shade_color, edgecolor='black')    

    # plt.text(LoR_value_position[0], LoR_value_position[1], 
    #          r'$LoR_{sys, %s} = %s %s $' % (rs_abbreviation, round(LoR_value, 2), rs_unit),                   
    #          bbox=bbox_LoR, transform=ax.transAxes, 
    #          horizontalalignment='right',
    #          verticalalignment='bottom')              
    plt.legend(loc="upper right", 
                bbox_to_anchor = (legend_position[0], legend_position[1]),                   
                frameon=True, facecolor = 'white',
                edgecolor = 'black')    
    # add an arrow to show the disaster
    ax.annotate('Disaster', xy=(0, 100), xytext=(0, 112),
        arrowprops=dict(facecolor='red', shrink=1.0),
        bbox=dict(boxstyle='square', facecolor='white'),
        horizontalalignment='center')
    
    # save the figure
    savename = 'dummy_LoR_plot_supply_only.png'    
    plt.savefig(savename, dpi=150)
   
    plt.plot(time_series, total_demand_with_warmup, 
                label=r'$D_{sys, %s}$' % (rs_abbreviation), color = 'red') 
    plt.legend(loc="upper right", 
                bbox_to_anchor = (legend_position[0], legend_position[1]),                   
                frameon=True, facecolor = 'white',
                edgecolor = 'black')        

    savename = 'dummy_LoR_plot_supply_demand.png'
    plt.savefig(savename, dpi=150) 

    plt.plot(time_series, total_consumption_with_warmup, 
                label=r'$C_{sys, %s}$' % (rs_abbreviation), color = 'green')       

    
    plt.legend(loc="upper right", 
                bbox_to_anchor = (legend_position[0], legend_position[1]),                   
                frameon=True, facecolor = 'white',
                edgecolor = 'black')    
    
    savename = 'dummy_LoR_plot_supply_demand_consumption.png'
    plt.savefig(savename, dpi=150)

    # add the shading between demand and consumption
    plt.fill_between(time_series, 
                        total_demand_with_warmup, 
                        total_consumption_with_warmup, 
                        label=r'$LoR_{sys, %s}$' % (rs_abbreviation),
                        color=LoR_shade_color, alpha=0.2) 

    plt.legend(loc="upper right", 
                bbox_to_anchor = (legend_position[0], legend_position[1]),                   
                frameon=True, facecolor = 'white',
                edgecolor = 'black')    

    savename = 'dummy_LoR_plot_supply_demand_consumption_LoR.png'
    plt.savefig(savename, dpi=150) 

double_LoR_illustration_plot = False

if double_LoR_illustration_plot:
    supply_1 = np.asarray([100, 20, 20, 100, 100, 100, 100, 100, 100, 100, 100])
    demand_1 = np.asarray([90, 60, 60, 90, 90, 90, 90, 90, 90, 90, 90])
    consumption_1 = np.asarray([90, 0, 0, 90, 90, 90, 90, 90, 90, 90, 90])
    max_time_step = len(supply_1)
    time_series = np.arange(max_time_step)
    rs_abbreviation = 'R/S'
    legend_position = [0.97, 0.3]
    # Plotting using MATPLOTLIB       
    plt.style.use('seaborn')      

    # add 1 time steps before the disaster
    warmup = 1
    time_series = np.arange(-warmup, max_time_step)
    LoR_shade_color = (0, 0.75, 1, 0.5)       
                
    plt.Figure(figsize=(8, 4), dpi=150)
    # independent values
    total_supply_with_warmup = np.concatenate((np.repeat(supply_1[0], warmup), supply_1[:]), axis = 0)
    total_demand_with_warmup = np.concatenate((np.repeat(demand_1[0], warmup), demand_1[:]), axis = 0)
    total_consumption_with_warmup = np.concatenate((np.repeat(consumption_1[0], warmup), consumption_1[:]), axis = 0)
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
    plt.xlabel(r'$Time \ Step$')
    plt.ylabel(r'$Demand,\  Supply\  Capacity,\  Consumption$')
    plt.xlim([-warmup, max_time_step-1])
    ticks = [0 ,2, 4, 6, 8, 10]
    labels = [r'$0 = t_{0}$', '2', '4', '6', '8', r'$10 = t_{f}$']
    ax = plt.gca()
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    plt.ylim([0, max(1.2*max(total_demand_with_warmup), 1.2*max(total_supply_with_warmup))])
    # set the text box
    bbox_LoR = dict(boxstyle="square", facecolor=LoR_shade_color, edgecolor='black')    

    # plt.text(LoR_value_position[0], LoR_value_position[1], 
    #          r'$LoR_{sys, %s} = %s %s $' % (rs_abbreviation, round(LoR_value, 2), rs_unit),                   
    #          bbox=bbox_LoR, transform=ax.transAxes, 
    #          horizontalalignment='right',
    #          verticalalignment='bottom')              
    plt.legend(loc="upper right", 
                bbox_to_anchor = (legend_position[0], legend_position[1]),                   
                frameon=True, facecolor = 'white',
                edgecolor = 'black')    
    # add an arrow to show the disaster
    ax.annotate('Disaster', xy=(0, 100), xytext=(0, 112),
        arrowprops=dict(facecolor='red', shrink=1.0),
        bbox=dict(boxstyle='square', facecolor='white'),
        horizontalalignment='center')
    
    # save the figure
    savename = 'dummy_LoR_plot_type_1.png'
    plt.savefig(savename, dpi=150, bbox_inches = 'tight') 
    plt.close()


    supply_2 = np.asarray([100, 80, 80, 80, 80, 80, 100, 100, 100, 100, 100])
    demand_2 = np.asarray([90, 70, 70, 70, 70, 70, 70, 90, 90, 90, 90])
    consumption_2 = np.asarray([90, 40,40, 40, 40, 40, 40, 90, 90, 90, 90])
    max_time_step = len(supply_2)
    time_series = np.arange(max_time_step)
    rs_abbreviation = 'R/S'
    legend_position = [0.97, 0.3]
    # Plotting using MATPLOTLIB       
    plt.style.use('seaborn')      

    # add 1 time steps before the disaster
    warmup = 1
    time_series = np.arange(-warmup, max_time_step)
    LoR_shade_color = (0, 0.75, 1, 0.5)       
                
    plt.Figure(figsize=(8, 4), dpi=150)
    # independent values
    total_supply_with_warmup = np.concatenate((np.repeat(supply_2[0], warmup), supply_2[:]), axis = 0)
    total_demand_with_warmup = np.concatenate((np.repeat(demand_2[0], warmup), demand_2[:]), axis = 0)
    total_consumption_with_warmup = np.concatenate((np.repeat(consumption_2[0], warmup), consumption_2[:]), axis = 0)
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
    plt.xlabel(r'$Time \ Step$')
    plt.ylabel(r'$Demand,\  Supply\  Capacity,\  Consumption$')
    plt.xlim([-warmup, max_time_step-1])
    ticks = [0 ,2, 4, 6, 8, 10]
    labels = [r'$0 = t_{0}$', '2', '4', '6', '8', r'$10 = t_{f}$']
    ax = plt.gca()
    ax.set_xticks(ticks)
    ax.set_xticklabels(labels)
    plt.ylim([0, max(1.2*max(total_demand_with_warmup), 1.2*max(total_supply_with_warmup))])
    # set the text box
    bbox_LoR = dict(boxstyle="square", facecolor=LoR_shade_color, edgecolor='black')  

    plt.legend(loc="upper right", 
                bbox_to_anchor = (legend_position[0], legend_position[1]),                   
                frameon=True, facecolor = 'white',
                edgecolor = 'black')    
    # add an arrow to show the disaster
    ax.annotate('Disaster', xy=(0, 100), xytext=(0, 112),
        arrowprops=dict(facecolor='red', shrink=1.0),
        bbox=dict(boxstyle='square', facecolor='white'),
        horizontalalignment='center')
   
    # save the figure
    savename = 'dummy_LoR_plot_type_2.png'
    plt.savefig(savename, dpi=150, bbox_inches = 'tight') 
    