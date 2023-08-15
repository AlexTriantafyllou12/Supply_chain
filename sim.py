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

# generate demand per SKU
demand = funcs.generate_demand(
    nr_SKUs=nr_SKUs,
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

#for sample_inventory_policies:
 # SKU0 = periodic review, order up to a point
 # SKU1 = reorder once inventory levels reach reorder point (rop), constant quantity
 # SKU2 = reorder once inventory levels reach rop, order up to a point
 # SKU3 = reorder once inventory levels reach rop, constant quantity
 # SKU4 = periodic review, constant quantity

policy_types = ["max", "const", "max", "const", "max"]

periodic_review_SKUs = [0, 4]
continuous_review_SKUs = [1,2,3]

# simulate SKUs with a continous review policy
for sku in range(len(continuous_review_SKUs)):
    sku_index = continuous_review_SKUs[sku]
    sim_results["SKU_"+str(continuous_review_SKUs[sku])] = {}

    for s in range(nr_sims):
        # random sampling of max and constant quantity values 
        max_quantities = [random.choice(max_quantity) for i in range(len(continuous_review_SKUs))]
        constant_quantities = [random.choice(contant_quantity) for i in range(len(continuous_review_SKUs))]
        
        # run the simulation
        output = funcs.inventory_sim(
                    time_periods=time_periods,
                    max_quantity=max_quantities[sku],
                    constant_quantity=constant_quantities[sku],
                    starting_inventory=starting_inventory[sku_index],
                    rop=rop[sku_index],
                    lead_time=lead_time_mean[sku_index%2],
                    per_item_cost=per_item_cost,
                    holding_costs=holding_costs,
                    delivery_cost=delivery_cost,
                    stock_out_cost=stock_out_cost,
                    demand=demand[sku_index],
                    policy_type=policy_types[sku_index])
        
        sim_results["SKU_"+str(continuous_review_SKUs[sku])]["s_"+str(s)] = output


df_output = pd.DataFrame()

# convert the nested results dicionary into a dataframe
for key in sim_results.keys():
    for sub_key in sim_results[key].keys():

        df =pd.DataFrame.from_dict(sim_results[key][sub_key],orient='index')
        df["Simulation"] = sub_key
        df["SKU"] = key
        df_output = pd.concat([df_output, df])

df_output.to_csv('data/sim_results.csv', index=False)