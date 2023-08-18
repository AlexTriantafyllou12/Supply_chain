import funcs
import random
import numpy as np
import configparser
import pandas as pd

# import global varibale from a config file
config = configparser.ConfigParser()
config.read('sim.config')
global_variables = config['global']

lead_time_mean = np.array(list(global_variables['lead_time_mean']), dtype=int)
lead_time_sd = np.array(list(global_variables['lead_time_sd']), dtype=int)

nr_SKUs = int(global_variables['nr_SKUs'])
nr_suppliers = int(global_variables['nr_suppliers'])

nr_sims = int(global_variables['nr_sims'])

holding_costs = float(global_variables['holding_costs']) # percent of the total cost of the item stored
delivery_cost = int(global_variables['delivery_cost']) # constant per delivery
stock_out_cost = int(global_variables['stock_out_cost'])
per_item_cost = int(global_variables['per_item_cost'])
time_periods = int(global_variables['time_periods'])

# define demand mean/ sd based on the number of SKUs
demand_mean = [random.randint(300, 600) for i in range(nr_SKUs)]
demand_sd = [random.randint(50, 100) for i in range(nr_SKUs)]

sim_results = {} # simulation results will go here
sim_config = {} # simulation configuration data will go here

# generate demand per SKU
demand = funcs.generate_demand(
    nr_SKUs=nr_SKUs,
    distribution_type=["norm", "poisson", "norm", "binomial", "poisson"],
    frequency=[1, 1, 7, 3, 1],
    time_periods=time_periods,
    demand_mean=demand_mean,
    demand_sd=demand_sd
)

safety_stocks = np.asarray([funcs.find_safety_stock( 
                          demand_mean=demand_mean[i],
                          demand_sd=demand_sd[i],
                          lead_time_mean=lead_time_mean[i%2], # even SKUs delivered by suppplier 1 (index = 0), odd SKUs delivered by supplier 2 (index = 1)
                          lead_time_sd=lead_time_sd[i%2]  
                        ) for i in range(nr_SKUs)])

rop = np.asarray([funcs.find_reorder_point(
                    demand_mean=demand_mean[i],
                    safety_stock=safety_stocks[i],
                    lead_time_mean=lead_time_mean[i%2]
                    ) for i in range(nr_SKUs)])

# assume starting inventory is 3 times the reorder point
starting_inventory = np.asarray([rop[i] * 2 for i in range(nr_SKUs)])

# sampling population for the periodic review policy
periodic_review_periods = np.arange(1,90,1)

# sampling population for the 'order up to a point' policy
max_quantity = np.arange(4000, 20000, 500)

# sampling population for the 'constant quantity' policy
contant_quantity = np.arange(500, 20000, 500)

# sampling population for the delivery lead times
delivery_lead_time = np.arange(2, 14, 1)

sim_results, sim_config = funcs.inventory_sim(
        simulations = nr_sims,
        time_periods = time_periods,
        delivery_cost=delivery_cost,
        nr_SKUs = nr_SKUs,
        nr_suppliers=nr_suppliers,
        starting_inventory = starting_inventory,
        rop = rop,
        per_item_cost = [[[0, 50, 0.9], [51, 120, 0.7], [121, 1000000, 0.6]], [[0, 50, 0.99], [51, 120, 0.88], [121, 100000, 0.6]], [[0, 100, 0.9], [101, 300, 0.7], [301, 100000, 0.6]], [[0, 100, 0.9], [101, 300, 0.7], [301, 100000, 0.6]], [[0, 100, 0.9], [101, 300, 0.7], [301, 100000, 0.6]]] ,
        holding_costs = 0.9,
        stock_out_cost = 1000000,
        demand=demand,
)


df_output = pd.DataFrame() # simulation results will go here
df_config = pd.DataFrame() # simulation configuration data will go here

for key in sim_results.keys():
    # convert the nested results and config dicionaries into dataframes
    for sub_key in sim_results[key].keys():
        df_c = pd.DataFrame.from_dict(sim_config[key][sub_key],orient='index')
        df_config = pd.concat([df_config, df_c])
        
        for sub_sub_key in sim_results[key][sub_key].keys():

            df = pd.DataFrame.from_dict(sim_results[key][sub_key][sub_sub_key],orient='index')
            df_output = pd.concat([df_output, df])

df_output.to_csv('data/sim_results.csv', index=False)
df_config.to_csv('data/sim_config.csv', index=False)

