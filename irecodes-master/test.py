import wntr
import numpy as np
import numpy as np
import System
import copy
import Priorities
import Plotting

    
# %% Script defines the virtual community used for the iReCoDeS paper (2020)

# %% Define considered R/Ss
considered_utilities = ['ElectricPower', 'HighLevelCommunication',
                                     'LowLevelCommunication', 'PotableWater', 
                                     'CoolingWater']

considered_transfer_services = ['ElectricPowerTransferService', 
                                'PotableWaterTransferService', 
                                'CoolingWaterTransferService',
                                'BridgeTransferService']

# %% Define shape file
num_localities = 21
x_coordinates = np.reshape([[i * 5 for i in range(int(num_localities/3))] for _ in range(3)], (-1)) # [km]
y_coordinates = np.reshape([[i * 5 for i in range(int(num_localities/7))] for _ in range(7)], (-1)) # [km]
shape = [{'LocalityID': i, 'Coord. X': x_coordinates[i-1], 'Coord. Y': y_coordinates[i-1], 'Content': dict()} for i in range(1, num_localities+1)]

# define locality contents  -->  add_reservoir()
shape[2]['Content'] = {'BSU': 2, 'BTS': 2, 'PWF': 1}     
shape[4]['Content'] = {'BSU': 3, 'BTS': 3, 'PWF': 1, 'CWF': 1, 'BSC': 1}
shape[14]['Content'] = {'EPP': 1, 'BTS': 1, 'CWF': 1}
shape[16]['Content'] = {'BSU': 3, 'BTS': 3, 'CWF': 1, 'BSC': 1, 'PWF': 1}
shape[18]['Content'] = {'EPP': 1, 'BTS': 1, 'CWF': 1}
shape[20]['Content'] = {'PWF': 1, 'BTS': 1, 'BSU': 1}


# define links - use Locality IDs to define this --> add_pipe()
shape[0]['LinkTo'] = {key: [2, 8] for key in ['CWP', 'PWP', 'EPTL']}
shape[1]['LinkTo'] = {key: [1, 9, 3] for key in ['CWP', 'PWP', 'EPTL']}
shape[2]['LinkTo'] = {key: [2, 10, 4] for key in ['CWP', 'PWP', 'EPTL']}
shape[3]['LinkTo'] = {key: [3, 5] for key in ['CWP', 'PWP', 'EPTL']}
shape[4]['LinkTo'] = {key: [4, 12, 6] for key in ['CWP', 'PWP', 'EPTL']}
shape[5]['LinkTo'] = {key: [5, 7, 13] for key in ['CWP', 'PWP', 'EPTL']}
shape[6]['LinkTo'] = {key: [6, 14] for key in ['CWP', 'PWP', 'EPTL']}
shape[7]['LinkTo'] = {key: [1, 9, 15] for key in ['CWP', 'PWP', 'EPTL']}
shape[8]['LinkTo'] = {key: [8, 2, 10] for key in ['CWP', 'PWP', 'EPTL']}
shape[9]['LinkTo'] = {key: [3, 9, 17] for key in ['CWP', 'PWP', 'EPTL']}
shape[11]['LinkTo'] = {key: [5, 19, 13] for key in ['CWP', 'PWP', 'EPTL']}
shape[12]['LinkTo'] = {key: [6, 12, 14, 20] for key in ['CWP', 'PWP', 'EPTL']}
shape[13]['LinkTo'] = {key: [7, 13, 21] for key in ['CWP', 'PWP', 'EPTL']}
shape[14]['LinkTo'] = {key: [8, 16] for key in ['CWP', 'PWP', 'EPTL']}
shape[15]['LinkTo'] = {key: [15, 17] for key in ['CWP', 'PWP', 'EPTL']}
shape[16]['LinkTo'] = {key: [10, 16, 18] for key in ['CWP', 'PWP', 'EPTL']}
shape[17]['LinkTo'] = {key: [17, 19] for key in ['CWP', 'PWP', 'EPTL']}
shape[18]['LinkTo'] = {key: [18, 12, 20] for key in ['CWP', 'PWP', 'EPTL']}
shape[19]['LinkTo'] = {key: [19, 13, 21] for key in ['CWP', 'PWP', 'EPTL']}
shape[20]['LinkTo'] = {key: [14, 20] for key in ['CWP', 'PWP', 'EPTL']}

shape[0]['Coord. X'] = 0
shape[0]['Coord. Y'] = 0
shape[1]['Coord. X'] = 5
shape[1]['Coord. Y'] = 0
shape[2]['Coord. X'] = 10
shape[2]['Coord. Y'] = 0
shape[3]['Coord. X'] = 15
shape[3]['Coord. Y'] = 0
shape[4]['Coord. X'] = 20
shape[4]['Coord. Y'] = 0
shape[5]['Coord. X'] = 25
shape[5]['Coord. Y'] = 0
shape[6]['Coord. X'] = 30
shape[6]['Coord. Y'] = 0
shape[7]['Coord. X'] = 0
shape[7]['Coord. Y'] = 5
shape[8]['Coord. X'] = 5
shape[8]['Coord. Y'] = 5
shape[9]['Coord. X'] = 10
shape[9]['Coord. Y'] = 5
shape[11]['Coord. X'] = 20
shape[11]['Coord. Y'] =5
shape[12]['Coord. X'] =25 
shape[12]['Coord. Y'] =5
shape[13]['Coord. X'] =30
shape[13]['Coord. Y'] =5
shape[14]['Coord. X'] =0
shape[14]['Coord. Y'] =10
shape[15]['Coord. X'] =5
shape[15]['Coord. Y'] =10
shape[16]['Coord. X'] =10
shape[16]['Coord. Y'] =10
shape[17]['Coord. X'] =15
shape[17]['Coord. Y'] =10
shape[18]['Coord. X'] =20
shape[18]['Coord. Y'] =10
shape[19]['Coord. X'] =25
shape[19]['Coord. Y'] =10
shape[20]['Coord. X'] =30
shape[20]['Coord. Y'] =10


#shape[id][atrtribute] = value
# lengths = [x,y,z,..] 
# for i in range(0,21):
#    shape[i][length] = lenghts[i]

# define bridges - bridges should be define in the locality where the links appear for the first time!
shape[14]['BridgeTo'] = {key: [8, 16] for key in ['CWP', 'PWP', 'EPTL']}
shape[7]['BridgeTo'] = {key: [15] for key in ['CWP', 'PWP', 'EPTL']}
shape[15]['BridgeTo'] = {key: [15] for key in ['CWP', 'PWP', 'EPTL']}

# define potential paths - elements of the lists are localities over which the path passes
potential_paths = dict()
potential_paths['ElectricPowerTransferService'] = {'from 3 to 5': [[3, 4, 5], [3, 10, 17, 18, 19, 12, 5]], 
                                                   'from 3 to 15': [[3, 2, 1, 8, 15], [3, 10, 17, 16, 15], [3, 10, 9, 8, 15]],
                                                   'from 3 to 17': [[3, 10, 17], [3, 4, 5, 12, 19, 18, 17], [3, 2, 1, 8, 15, 16, 17]],
                                                   'from 3 to 19': [[3, 10, 17, 18, 19], [3, 4, 5, 12, 19]],
                                                   'from 3 to 21': [[3, 10, 17, 18, 19, 20, 21], [3, 4, 5, 12, 19, 20, 21], [3, 4, 5, 6, 7, 8, 14, 21]],
                                                   'from 5 to 3': [[5, 4, 3], [5, 12, 19, 18, 17, 10, 3]],
                                                   'from 5 to 15': [[5, 4, 3, 2, 1, 8, 15], [5, 4, 3, 10, 17, 16, 15], [5, 12, 19, 18, 17, 16, 15]],
                                                   'from 5 to 17': [[5, 4, 3, 10, 17], [5, 12, 19, 18, 17]],
                                                   'from 5 to 19': [[5, 12, 19], [5, 6, 13, 20, 19], [5, 12, 13, 20, 19]],
                                                   'from 5 to 21': [[5, 12, 19, 20, 21], [5, 12, 13, 20, 21], [5, 6, 7, 14, 21]],
                                                   'from 15 to 3': [[15, 8, 1, 2, 3], [15, 16, 17, 10, 3], [15, 8, 9, 10, 3]],
                                                   'from 15 to 5': [[15, 8, 1, 2, 3, 4, 5], [15, 16, 17, 10, 3, 4, 5], [15, 16, 17, 18, 19, 12, 5]],
                                                   'from 15 to 17': [[15, 16, 17], [15, 8, 9, 10, 17], [ 15, 8, 1, 2, 3, 10, 17]],
                                                   'from 15 to 19': [[15, 16, 17, 18, 19], [15, 8, 9, 10, 17, 18, 19], [15, 8, 1, 2, 3, 4, 5, 12, 19]],
                                                   'from 15 to 21': [[15, 16, 17, 18, 19, 20, 21], [15, 8, 1, 2, 3, 4, 5, 6, 7, 14, 21]],
                                                   'from 17 to 3': [[17, 10, 3], [17, 18, 19, 12, 5, 4, 3], [17, 16, 15, 8, 1, 2, 3]],
                                                   'from 17 to 5': [[17, 10, 3, 4, 5], [17, 18, 19, 12, 5]],
                                                   'from 17 to 15': [[17, 16, 15], [17, 10, 9, 8, 15], [17, 10, 3, 2, 1, 8, 15]],
                                                   'from 17 to 19': [[17, 18, 19], [17, 10, 3, 4, 5, 12, 19]],
                                                   'from 17 to 21': [[17, 18, 19, 20, 21], [17, 10, 3, 4, 5, 6, 7, 14, 21]],
                                                   'from 19 to 3': [[19, 18, 17, 10, 3], [19, 12, 5, 4, 3]],
                                                   'from 19 to 5': [[19, 12, 5], [19, 20, 13, 6, 5], [19, 20, 13, 12, 5]],
                                                   'from 19 to 15': [[19, 18, 17, 16, 15], [19, 18, 17, 10, 9, 8, 15], [19, 12, 5, 4, 3, 2, 1, 8, 15]],
                                                   'from 19 to 17': [[19, 18, 17], [19, 12, 5, 4, 3, 10, 17]],
                                                   'from 19 to 21': [[19, 20, 21], [19, 12, 13, 14, 21], [19, 12, 5, 6, 7, 14, 21]],
                                                   'from 21 to 3': [[21, 20, 19, 18, 17, 10, 3], [21, 20, 19, 12, 5, 4, 3], [21, 14, 8, 7, 6, 5, 4, 3]],
                                                   'from 21 to 5': [[21, 20, 19, 12, 5], [21, 20, 13, 12, 5], [21, 14, 7, 6, 5]],
                                                   'from 21 to 15': [[21, 20, 19, 18, 17, 16, 15], [21, 14, 7, 6, 5, 4, 3, 2, 1, 8, 15]],
                                                   'from 21 to 17': [[21, 20, 19, 18, 17], [21, 14, 7, 6, 5, 4, 3, 10, 17]],
                                                   'from 21 to 19': [[21, 20, 19], [21, 14, 13, 12, 19], [21, 14, 7, 6, 5, 12, 19]]}


# assume the same potential paths for all transfer services
potential_paths['CoolingWaterTransferService'] = potential_paths['ElectricPowerTransferService']
potential_paths['PotableWaterTransferService'] = potential_paths['ElectricPowerTransferService']

# %% Define damage - use the same damage as in the iReCoDeS paper
 #damage_vector = np.random.rand(117)
## initial damage
damage_vector = [0.27, 0.35, 0.27, 0.35, 0.19, 0.47, 0.25, 0.15, 0.25, 0.15, 0.34, 0.49, 0.42, 0.44, 
                 0.44, 0.03, 0.55, 0.45, 0.45, 0.45, 0.45, 0.42, 0.45, 0.06, 0.06, 0.19, 0.53, 0.13, 
                 0.51, 0.3, 0.62, 0.2, 0.27, 0.62, 0.33, 0.03, 0.1, 0.03, 0.1, 0.33, 0.05, 0.22, 0.02, 
                 0.22, 0.02, 0.05, 0.18, 0.23, 0.23, 0.11, 0.32, 0.5, 0.14, 0.32, 0.14, 0.2, 0.23, 0.34, 
                 0.34, 0.13, 0.01, 0.01, 0.23, 0.13, 0.28, 0.13, 0.28, 0.29, 0.43, 0.21, 0.14, 0.21, 0.14, 
                 0.14, 0.14, 0.35, 0.35, 0.23, 0.18, 1.0, 1.0, 0.0, 0.22, 0.22, 0.1, 0.08, 0.08, 0.1, 0.1, 
                 0.13, 0.6, 0.51, 0.08, 0.85, 0.43, 0.49, 0.07, 0.27, 0.27, 0.1, 0.39, 0.39, 0.1, 0.6, 1.0, 
                 1.0, 0.15, 0.15, 0.24, 0.11, 0.11, 0.18, 0.47, 0.35, 0.2]

# 0 = no damage
# 1 = complete damage

def get_demand_value (node, type, conversion = True):
    default_demand_value = 0.086
    if (len(shape[node]['Content']) == 0):
        return 'no content'
    if conversion:
        return default_demand_value * shape[node]['Content'].get(type) * 0.011574074074074 # conversion from ML/d to m^3/s
    return default_demand_value * shape[node]['Content'].get(type)

def get_supply_value (node, type, conversion = True):
    default_supply_value = -0.2
    if (len(shape[node]['Content']) == 0):
        return 'no content'
    if conversion:
        return default_supply_value * shape[node]['Content'].get(type) * 0.011574074074074 # conversion from ML/d to m^3/s
    return default_supply_value * shape[node]['Content'].get(type)


def network(): ## and no pumps
    ## Define network

    wn = wntr.network.WaterNetworkModel()
    add_pipes_to = []
    supply_pwf = 0
    for i in range(0,21):
        if (i == 10):
            continue
        if (len(shape[i]['Content']) != 0):
            if ('BSU' in shape[i]['Content']):
                calculated_base_demand = get_demand_value(i, 'BSU', True)
                wn.add_junction('N'+str(i), base_demand = calculated_base_demand, coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            else:
                wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            if ('PWF' in shape[i]['Content']):
                calculated_supply = get_supply_value(i, 'PWF', True)
                supply_pwf += calculated_supply
                wn.add_reservoir('RES'+str(i), coordinates=(shape[i]['Coord. X']+2,shape[i]['Coord. Y']+2))
                wn.add_junction('PWFn'+str(i), base_demand = calculated_supply, coordinates=(shape[i]['Coord. X']+1,shape[i]['Coord. Y']+1))
                add_pipes_to.append(str(i))
        else:
            wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
    
    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_pipe('f'+str(i)+'t'+str(linkto-1),'N'+str(i),'N'+str(linkto-1),diameter =10) # Default pipe diameter = 0.3046m -> increased in order to simulate infinite transfer capacity of pipes
        for res in add_pipes_to:
            wn.add_pipe('RES'+str(res)+'PWFn'+str(res),'RES'+str(res),'PWFn'+str(res)) 
            wn.add_pump('pumpf'+str(res)+'pumpt'+str(res),'RES'+str(res),'PWFn'+str(res)) 
            wn.add_pipe('PWFn'+str(res)+'tr'+str(res),'PWFn'+str(res),'N'+str(res))
            wn.add_pipe('fn'+str(res)+'PWFn'+str(res),'N'+str(res),'PWFn'+str(res))
    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_valve('v' + str(i) + str(linkto-1),'N'+str(i),'N'+str(linkto-1), valve_type='FCV')
            wn.add_valve('v' + str(linkto-1) + str(i),'N'+str(linkto-1),'N'+str(i), valve_type='FCV')
    
    ## Simulate hydraulics

    wn.options.hydraulic.demand_model = 'PDD' # PDD or DD
    sim = wntr.sim.WNTRSimulator(wn)    # WNTRSimulator or EpanetSimulator
    results = sim.run_sim()
    pressure = results.node['pressure']
    required_pressure = wn.options.hydraulic.required_pressure

    ## Check flow of water: if pressure < required_pressure -> junction will not receive full water demand

    for i in range(0,21):
        if (i == 10):
            continue
        if (pressure.loc[:,'N'+str(i)][0] < required_pressure):
            print('Pressure does not exceed required_pressure'+str(i))
        else:
            print('Pressure exceeds required_pressure'+str(i))

    ## Check that suppliers can meet demand of BSU
    
    demand = results.node['demand']
    leak_demand = results.node['leak_demand']
    flowrate = results.link['flowrate'] #get.node for demand, pressure, leak demand, head or get.link for the velocity, flowrate, headloss
    pwfs = [2,4,16,20]
    total_pwf_supply = 0
    total_BSU_demand = 0
    for i in pwfs:
        total_pwf_supply = total_pwf_supply + demand.loc[:,'PWFn'+str(i)][0]+demand.loc[:,'RES'+str(i)][0]
        total_BSU_demand += demand.loc[:,'N'+str(i)][0]
    if (total_pwf_supply*-1 < supply_pwf*-1):
        print("PWFs can supply demand")
    else:
        print("PWFs can not supply demand")
    print(demand.head())
    leak_demand.to_excel('leak_demand.xlsx')
    #print(total_pwf_supply*-1)
    #print(supply_pwf*-1)
    #print(total_BSU_demand)


#network()
## Damaged Networks:
    # PWFs fully damage : t0
    # PWF2 repaired: t5
    # PWF4 repaired: t8
    # PWF16 repaired: t12
    # PWF20 repaired: t15

damage_vector_t0 = [1,1,1,1] # functionality 0
def damaged_network_t0():
    dwert = 0
    dwert_t0 =0
    supply_pwf = 0
    wn = wntr.network.WaterNetworkModel()
    add_pipes_to = []
    for i in range(0,21):
        if (i == 10):
            continue
        if (len(shape[i]['Content']) != 0):
            if ('BSU' in shape[i]['Content']):
                calculated_base_demand = get_demand_value(i, 'BSU', True)
                calculated_base_demand *= (1-damage_vector[dwert]) #The influence of damage on the supply capacity is considered by multiplying the current functionality level of the component with its supply capacity at full functionality. 
                dwert+=1
                wn.add_junction('N'+str(i), base_demand = calculated_base_demand, coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            else:
                wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            if ('PWF' in shape[i]['Content']):
                calculated_supply = get_supply_value(i, 'PWF', True)
                calculated_supply *=(1-damage_vector_t0[dwert_t0])
                supply_pwf += calculated_supply
                dwert_t0+=1
                wn.add_reservoir('RES'+str(i), coordinates=(shape[i]['Coord. X']+2,shape[i]['Coord. Y']+2))
                wn.add_junction('PWFn'+str(i), base_demand = calculated_supply, coordinates=(shape[i]['Coord. X']+1,shape[i]['Coord. Y']+1))
                add_pipes_to.append(str(i))
        else:
            wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
    
    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_pipe('f'+str(i)+'t'+str(linkto-1),'N'+str(i),'N'+str(linkto-1),diameter =10)
            wn = wntr.morph.split_pipe(wn,'f'+str(i)+'t'+str(linkto-1), 'f'+str(i)+'t'+str(linkto-1)+'_L', 'f'+str(i)+'t'+str(linkto-1)+'Leak' )
            pipe = wn.get_node('f'+str(i)+'t'+str(linkto-1)+'Leak')
            calculated_discharge_coeff = damage_vector[dwert] ## reducing the demand leak means reducing the damage level
            dwert+=1
            pipe.add_leak(wn, discharge_coeff=calculated_discharge_coeff, area=0.05) # area: from example of WNTR documentation, discharge_coeff: default = 0.75
        for res in add_pipes_to:
            #wn.add_pipe('RES'+str(res)+'PWFn'+str(res),'RES'+str(res),'PWFn'+str(res)) #it is only by removing the pipes and pumps linking the RES to the PWFS that full damage to the system can be simulated. changing the initial_status of the pipes or pumps to 'CLOSED' does not work
            #wn.add_pump('pumpf'+str(res)+'pumpt'+str(res),'RES'+str(res),'PWFn'+str(res)) 
            wn.add_pipe('PWFn'+str(res)+'tr'+str(res),'PWFn'+str(res),'N'+str(res))
            wn.add_pipe('fn'+str(res)+'PWFn'+str(res),'N'+str(res),'PWFn'+str(res))

    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_valve('v' + str(i) + str(linkto-1),'N'+str(i),'N'+str(linkto-1), valve_type='FCV')
            wn.add_valve('v' + str(linkto-1) + str(i),'N'+str(linkto-1),'N'+str(i), valve_type='FCV')
    
    wntr.graphics.plot_network(wn, node_alpha=0, node_labels=True, title='Case Study Network', link_alpha=0)
   
    #Simulate hydraulics
    wn.options.hydraulic.demand_model = 'PDD' # PDD or DD
    sim = wntr.sim.WNTRSimulator(wn)    # WNTRSimulator or EpanetSimulator
    results = sim.run_sim()
    pressure = results.node['pressure']
    required_pressure = wn.options.hydraulic.required_pressure

    ## Check flow of water: if pressure < required_pressure -> junction will not receive full water demand
    for i in range(0,21):
        if (i == 10):
            continue
        if (pressure.loc[:,'N'+str(i)][0] < required_pressure):
            print('Pressure does not exceed required_pressure'+str(i))
        else:
            print('Pressure exceeds required_pressure'+str(i))

    demand = results.node['demand']
    pwfs = [2,4,16,20]
    total_pwf_supply = 0
    for i in pwfs:
        total_pwf_supply = total_pwf_supply + demand.loc[:,'PWFn'+str(i)][0]+demand.loc[:,'RES'+str(i)][0]
    if (total_pwf_supply*-1 < supply_pwf*-1):
        print("PWFs can supply demand")
    else:
        print("PWFs can not supply demand")
    demand = results.node['demand'] #get.node for demand, pressure, leak demand, head or get.link for the velocity, flowrate, headloss
    print(demand.head())
    demand.to_excel('demand_damaged.xlsx')
    # demand = demand from Junction 0-20
    # supply = negative demand from PWFs 2,4,16,20
    print(total_pwf_supply*-1)
    print(supply_pwf*-1) # =0 here, because all PWF are damaged 

#damaged_network_t0()

damage_vector_t5 = [0,1,1,1]
def damaged_network_t5():
    dwert = 0
    dwert_t5 = 0
    supply_pwf = 0
    wn = wntr.network.WaterNetworkModel()
    add_pipes_to = []
    for i in range(0,21):
        if (i == 10):
            continue
        if (len(shape[i]['Content']) != 0):
            if ('BSU' in shape[i]['Content']):
                calculated_base_demand = get_demand_value(i, 'BSU', True)
                calculated_base_demand *= (1-damage_vector[dwert])
                dwert+=1
                wn.add_junction('N'+str(i), base_demand = calculated_base_demand, coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            else:
                wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            if ('PWF' in shape[i]['Content']):
                calculated_supply = get_supply_value(i, 'PWF', True)
                calculated_supply *=(1-damage_vector_t5[dwert_t5])
                supply_pwf += calculated_supply
                dwert_t5+=1
                wn.add_reservoir('RES'+str(i), coordinates=(shape[i]['Coord. X']+2,shape[i]['Coord. Y']+2))
                wn.add_junction('PWFn'+str(i), base_demand = calculated_supply, coordinates=(shape[i]['Coord. X']+1,shape[i]['Coord. Y']+1))
                add_pipes_to.append(str(i))
        else:
            wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
    
    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_pipe('f'+str(i)+'t'+str(linkto-1),'N'+str(i),'N'+str(linkto-1),diameter =10)
            wn = wntr.morph.split_pipe(wn,'f'+str(i)+'t'+str(linkto-1), 'f'+str(i)+'t'+str(linkto-1)+'_L', 'f'+str(i)+'t'+str(linkto-1)+'Leak' )
            pipe = wn.get_node('f'+str(i)+'t'+str(linkto-1)+'Leak')
            calculated_discharge_coeff = damage_vector[dwert] ## reducing the demand leak means reducing the damage level
            dwert+=1
            pipe.add_leak(wn, discharge_coeff=calculated_discharge_coeff, area=0.05) # area: from example of WNTR documentation, discharge_coeff: default = 0.75
        for res in add_pipes_to:
            wn.add_pipe('RES'+str(res)+'PWFn'+str(res),'RES'+str(res),'PWFn'+str(res)) #it is only by removing the pipes and pumps linking the RES to the PWFS that full damage to the system can be simulated. changing the initial_status of the pipes or pumps to 'CLOSED' does not work
            wn.add_pump('pumpf'+str(res)+'pumpt'+str(res),'RES'+str(res),'PWFn'+str(res)) 
            wn.add_pipe('PWFn'+str(res)+'tr'+str(res),'PWFn'+str(res),'N'+str(res))
            wn.add_pipe('fn'+str(res)+'PWFn'+str(res),'N'+str(res),'PWFn'+str(res))

    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_valve('v' + str(i) + str(linkto-1),'N'+str(i),'N'+str(linkto-1), valve_type='FCV')
            wn.add_valve('v' + str(linkto-1) + str(i),'N'+str(linkto-1),'N'+str(i), valve_type='FCV')
    
    wntr.graphics.plot_network(wn, node_alpha=0, node_labels=True, title='Case Study Network', link_alpha=0)
   
    #Simulate hydraulics
    wn.options.hydraulic.demand_model = 'PDD' # PDD or DD
    sim = wntr.sim.WNTRSimulator(wn)    # WNTRSimulator or EpanetSimulator
    results = sim.run_sim()
    pressure = results.node['pressure']
    required_pressure = wn.options.hydraulic.required_pressure

    ## Check flow of water: if pressure < required_pressure -> junction will not receive full water demand
    for i in range(0,21):
        if (i == 10):
            continue
        if (pressure.loc[:,'N'+str(i)][0] < required_pressure):
            print('Pressure does not exceed required_pressure'+str(i))
        else:
            print('Pressure exceeds required_pressure'+str(i))

    demand = results.node['demand']
    pwfs = [2,4,16,20]
    total_pwf_supply = 0
    for i in pwfs:
        total_pwf_supply += demand.loc[:,'PWFn'+str(i)][0]
    if (total_pwf_supply < supply_pwf):
        print("PWFs can supply demand")
    else:
        print("PWFs can not supply demand")
    demand = results.node['demand'] #get.node for demand, pressure, leak demand, head or get.link for the velocity, flowrate, headloss
    print(demand.head())
    demand.to_excel('demand_damaged.xlsx')
    
#damaged_network_t5()

damage_vector_t8 = [0,0,1,1]
def damaged_network_t8():
    dwert = 0
    dwert_t8 = 0
    supply_pwf = 0
    wn = wntr.network.WaterNetworkModel()
    add_pipes_to = []
    for i in range(0,21):
        if (i == 10):
            continue
        if (len(shape[i]['Content']) != 0):
            if ('BSU' in shape[i]['Content']):
                calculated_base_demand = get_demand_value(i, 'BSU', True)
                calculated_base_demand *= (1-damage_vector[dwert]+0.13) # reduce damage level by inceasing functionality
                dwert+=1
                wn.add_junction('N'+str(i), base_demand = calculated_base_demand, coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            else:
                wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            if ('PWF' in shape[i]['Content']):
                calculated_supply = get_supply_value(i, 'PWF', True)
                calculated_supply *=(1-damage_vector_t8[dwert_t8])
                supply_pwf += calculated_supply
                dwert_t8+=1
                wn.add_reservoir('RES'+str(i), coordinates=(shape[i]['Coord. X']+2,shape[i]['Coord. Y']+2))
                wn.add_junction('PWFn'+str(i), base_demand = calculated_supply, coordinates=(shape[i]['Coord. X']+1,shape[i]['Coord. Y']+1))
                add_pipes_to.append(str(i))
        else:
            wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
    
    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_pipe('f'+str(i)+'t'+str(linkto-1),'N'+str(i),'N'+str(linkto-1),diameter =10)
            wn = wntr.morph.split_pipe(wn,'f'+str(i)+'t'+str(linkto-1), 'f'+str(i)+'t'+str(linkto-1)+'_L', 'f'+str(i)+'t'+str(linkto-1)+'Leak' )
            pipe = wn.get_node('f'+str(i)+'t'+str(linkto-1)+'Leak')
            calculated_discharge_coeff = damage_vector[dwert] - 0.13
            dwert+=1
            pipe.add_leak(wn, discharge_coeff=calculated_discharge_coeff, area=0.05) # area: from example of WNTR documentation, discharge_coeff: default = 0.75
        for res in add_pipes_to:
            wn.add_pipe('RES'+str(res)+'PWFn'+str(res),'RES'+str(res),'PWFn'+str(res)) #it is only by removing the pipes and pumps linking the RES to the PWFS that full damage to the system can be simulated. changing the initial_status of the pipes or pumps to 'CLOSED' does not work
            wn.add_pump('pumpf'+str(res)+'pumpt'+str(res),'RES'+str(res),'PWFn'+str(res)) 
            wn.add_pipe('PWFn'+str(res)+'tr'+str(res),'PWFn'+str(res),'N'+str(res))
            wn.add_pipe('fn'+str(res)+'PWFn'+str(res),'N'+str(res),'PWFn'+str(res))

    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_valve('v' + str(i) + str(linkto-1),'N'+str(i),'N'+str(linkto-1), valve_type='FCV')
            wn.add_valve('v' + str(linkto-1) + str(i),'N'+str(linkto-1),'N'+str(i), valve_type='FCV')
    
    wntr.graphics.plot_network(wn, node_alpha=0, node_labels=True, title='Case Study Network', link_alpha=0)
   
    #Simulate hydraulics
    wn.options.hydraulic.demand_model = 'PDD' # PDD or DD
    sim = wntr.sim.WNTRSimulator(wn)    # WNTRSimulator or EpanetSimulator
    results = sim.run_sim()
    pressure = results.node['pressure']
    required_pressure = wn.options.hydraulic.required_pressure

    ## Check flow of water: if pressure < required_pressure -> junction will not receive full water demand
    for i in range(0,21):
        if (i == 10):
            continue
        if (pressure.loc[:,'N'+str(i)][0] < required_pressure):
            print('Pressure does not exceed required_pressure'+str(i))
        else:
            print('Pressure exceeds required_pressure'+str(i))

    demand = results.node['demand']
    pwfs = [2,4,16,20]
    total_pwf_supply = 0
    for i in pwfs:
        total_pwf_supply += demand.loc[:,'PWFn'+str(i)][0]
    if (total_pwf_supply < supply_pwf):
        print("PWFs can supply demand")
    else:
        print("PWFs can not supply demand")
    demand = results.node['demand'] #get.node for demand, pressure, leak demand, head or get.link for the velocity, flowrate, headloss
    print(demand.head())
    demand.to_excel('demand_damaged.xlsx')

#damaged_network_t8()

damage_vector_t12 = [0,0,0,1]
def damaged_network_t12():
    dwert = 0
    dwert_t12 = 0
    supply_pwf = 0
    wn = wntr.network.WaterNetworkModel()
    add_pipes_to = []
    for i in range(0,21):
        if (i == 10):
            continue
        if (len(shape[i]['Content']) != 0):
            if ('BSU' in shape[i]['Content']):
                calculated_base_demand = get_demand_value(i, 'BSU', True)
                calculated_base_demand *= (1-damage_vector[dwert]+0.29) # reduce damage level by inceasing functionality
                dwert+=1
                wn.add_junction('N'+str(i), base_demand = calculated_base_demand, coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            else:
                wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            if ('PWF' in shape[i]['Content']):
                calculated_supply = get_supply_value(i, 'PWF', True)
                calculated_supply *=(1-damage_vector_t12[dwert_t12])
                supply_pwf += calculated_supply
                dwert_t12+=1
                wn.add_reservoir('RES'+str(i), coordinates=(shape[i]['Coord. X']+2,shape[i]['Coord. Y']+2))
                wn.add_junction('PWFn'+str(i), base_demand = calculated_supply, coordinates=(shape[i]['Coord. X']+1,shape[i]['Coord. Y']+1))
                add_pipes_to.append(str(i))
        else:
            wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
    
    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_pipe('f'+str(i)+'t'+str(linkto-1),'N'+str(i),'N'+str(linkto-1),diameter =10)
            wn = wntr.morph.split_pipe(wn,'f'+str(i)+'t'+str(linkto-1), 'f'+str(i)+'t'+str(linkto-1)+'_L', 'f'+str(i)+'t'+str(linkto-1)+'Leak' )
            pipe = wn.get_node('f'+str(i)+'t'+str(linkto-1)+'Leak')
            calculated_discharge_coeff = damage_vector[dwert] - 0.29
            dwert+=1
            pipe.add_leak(wn, discharge_coeff=calculated_discharge_coeff, area=0.05) # area: from example of WNTR documentation, discharge_coeff: default = 0.75
        for res in add_pipes_to:
            wn.add_pipe('RES'+str(res)+'PWFn'+str(res),'RES'+str(res),'PWFn'+str(res)) #it is only by removing the pipes and pumps linking the RES to the PWFS that full damage to the system can be simulated. changing the initial_status of the pipes or pumps to 'CLOSED' does not work
            wn.add_pump('pumpf'+str(res)+'pumpt'+str(res),'RES'+str(res),'PWFn'+str(res)) 
            wn.add_pipe('PWFn'+str(res)+'tr'+str(res),'PWFn'+str(res),'N'+str(res))
            wn.add_pipe('fn'+str(res)+'PWFn'+str(res),'N'+str(res),'PWFn'+str(res))

    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_valve('v' + str(i) + str(linkto-1),'N'+str(i),'N'+str(linkto-1), valve_type='FCV')
            wn.add_valve('v' + str(linkto-1) + str(i),'N'+str(linkto-1),'N'+str(i), valve_type='FCV')
    
    wntr.graphics.plot_network(wn, node_alpha=0, node_labels=True, title='Case Study Network', link_alpha=0)
   
    #Simulate hydraulics
    wn.options.hydraulic.demand_model = 'PDD' # PDD or DD
    sim = wntr.sim.WNTRSimulator(wn)    # WNTRSimulator or EpanetSimulator
    results = sim.run_sim()
    pressure = results.node['pressure']
    required_pressure = wn.options.hydraulic.required_pressure

    ## Check flow of water: if pressure < required_pressure -> junction will not receive full water demand
    for i in range(0,21):
        if (i == 10):
            continue
        if (pressure.loc[:,'N'+str(i)][0] < required_pressure):
            print('Pressure does not exceed required_pressure'+str(i))
        else:
            print('Pressure exceeds required_pressure'+str(i))

    demand = results.node['demand']
    leak_demand = results.node['leak_demand']
    pwfs = [2,4,16,20]
    total_pwf_supply = 0
    for i in pwfs:
        total_pwf_supply += demand.loc[:,'PWFn'+str(i)][0]
    if (total_pwf_supply < supply_pwf):
        print("PWFs can supply demand")
    else:
        print("PWFs can not supply demand")
    demand = results.node['demand'] #get.node for demand, pressure, leak demand, head or get.link for the velocity, flowrate, headloss
    print(demand.head())
    demand.to_excel('demand_damaged.xlsx')

#damaged_network_t12()

damage_vector_t15 = [0,0,0,0]
def damaged_network_t15():
    
    dwert = 0
    dwert_t15 = 0
    supply_pwf = 0
    wn = wntr.network.WaterNetworkModel()
    wn.options.time.duration = 24*3600
    wn.options.time.hydraulic_timestep = 3600
    wn.options.time.report_timestep = 3600
    wn.options.hydraulic.demand_model = 'PDD'
    add_pipes_to = []
    for i in range(0,21):
        if (i == 10):
            continue
        if (len(shape[i]['Content']) != 0):
            if ('BSU' in shape[i]['Content']):
                calculated_base_demand = get_demand_value(i, 'BSU', True)
                calculated_base_demand *= (1-damage_vector[dwert]+0.46) # reduce damage level by inceasing functionality
                dwert+=1
                wn.add_junction('N'+str(i), base_demand = calculated_base_demand, coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            else:
                wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
            if ('PWF' in shape[i]['Content']):
                calculated_supply = get_supply_value(i, 'PWF', True)
                calculated_supply *=(1-damage_vector_t15[dwert_t15])
                supply_pwf += calculated_supply
                dwert_t15+=1
                wn.add_reservoir('RES'+str(i), coordinates=(shape[i]['Coord. X']+2,shape[i]['Coord. Y']+2))
                wn.add_junction('PWFn'+str(i), base_demand = calculated_supply, coordinates=(shape[i]['Coord. X']+1,shape[i]['Coord. Y']+1))
                add_pipes_to.append(str(i))
        else:
            wn.add_junction('N'+str(i), coordinates=(shape[i]['Coord. X'],shape[i]['Coord. Y']))
    
    directions = []
    for i in range(0,21):
        if (i == 10):
            continue
        for res in add_pipes_to:
            wn.add_pipe('RES'+str(res)+'PWFn'+str(res),'RES'+str(res),'PWFn'+str(res)) #it is only by removing the pipes and pumps linking the RES to the PWFS that full damage to the system can be simulated. changing the initial_status of the pipes or pumps to 'CLOSED' does not work
            wn.add_pump('pumpf'+str(res)+'pumpt'+str(res),'RES'+str(res),'PWFn'+str(res)) 
            wn.add_pipe('PWFn'+str(res)+'tr'+str(res),'PWFn'+str(res),'N'+str(res))
            wn.add_pipe('fn'+str(res)+'PWFn'+str(res),'N'+str(res),'PWFn'+str(res))

    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP
        for linkto in values:
            wn.add_valve('v' + str(i) + str(linkto-1),'N'+str(i),'N'+str(linkto-1), valve_type='FCV')
            wn.add_valve('v' + str(linkto-1) + str(i),'N'+str(linkto-1),'N'+str(i), valve_type='FCV')
    
    for i in range(0,21):
        if (i == 10):
            continue
        values = shape[i]['LinkTo'].get('PWP') # focus on PWP

        
        for linkto in values:
            directions += [(i+1,linkto)]

            wn.add_pipe('f'+str(i)+'t'+str(linkto-1),'N'+str(i),'N'+str(linkto-1),diameter =10)
            if (not (linkto,i+1) in directions):
                #print("omitted split at "+str(linkto)+" "+str(i+1))
                wn = wntr.morph.split_pipe(wn,'f'+str(i)+'t'+str(linkto-1), 'f'+str(i)+'t'+str(linkto-1)+'_L', 'f'+str(i)+'t'+str(linkto-1)+'Leak')
                pipe = wn.get_node('f'+str(i)+'t'+str(linkto-1)+'Leak')
                calculated_discharge_coeff = damage_vector[dwert]- 0.46 ## reducing the demand leak means reducing the damage level
                dwert+=1
                pipe.add_leak(wn, discharge_coeff=0.9, area=0.05, start_time=0,end_time=3600) # area: from example of WNTR documentation, discharge_coeff: default = 0.75


    wntr.graphics.plot_network(wn, node_alpha=0, node_labels=True, title='Case Study Network', link_alpha=0)
   
    #Simulate hydraulics
    wn.options.hydraulic.demand_model = 'PDD' # PDD or DD
    sim = wntr.sim.WNTRSimulator(wn)    # WNTRSimulator or EpanetSimulator
    results = sim.run_sim()
    pressure = results.node['pressure']
    required_pressure = wn.options.hydraulic.required_pressure

    ## Check flow of water: if pressure < required_pressure -> junction will not receive full water demand
    for i in range(0,21):
        if (i == 10):
            continue
        if (pressure.loc[:,'N'+str(i)][0] < required_pressure):
            print('Pressure does not exceed required_pressure'+str(i))
        else:
            print('Pressure exceeds required_pressure'+str(i))


    
    demand = results.node['demand']
    pwfs = [2,4,16,20]
    total_pwf_supply = 0
    for i in pwfs:
        total_pwf_supply += demand.loc[:,'PWFn'+str(i)][0]
    if (total_pwf_supply < supply_pwf):
        print("PWFs can supply demand")
    else:
        print("PWFs can not supply demand")
    demand = results.node['demand'] #get.node for demand, pressure, leak demand, head or get.link for the velocity, flowrate, headloss
    leak_demand = results.node['leak_demand']
    print(leak_demand.head())
    #print(directions)
    leak_demand.to_excel('leak_demand.xlsx')
    demand.to_excel('demand_damaged.xlsx')

damaged_network_t15()