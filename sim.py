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
sim_config = {} # simulation configuration data will go here

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

# simulate SKUs 
for sku in range(nr_SKUs):

    sim_results["SKU_"+str(sku)] = {}
    sim_config["SKU_"+str(sku)] = {}

    for s in range(nr_sims):
        # random sampling of max and constant quantity values 
        max_quantities = [random.choice(max_quantity) for i in range(nr_SKUs)]
        constant_quantities = [random.choice(contant_quantity) for i in range(nr_SKUs)]

        if sku in periodic_review_SKUs:
            # simulate different review periods
            for s1 in range(nr_sims):
                # random sampling for review periods 
                review_periods = [random.choice(periodic_review_periods) for i in range(nr_SKUs)]

                # run the simulation
                output = funcs.inventory_sim(
                            time_periods=time_periods,
                            max_quantity=max_quantities[sku],
                            review_period=review_periods[sku],
                            constant_quantity=constant_quantities[sku],
                            starting_inventory=starting_inventory[sku],
                            rop=rop[sku],
                            lead_time=lead_time_mean[sku%2],
                            per_item_cost=per_item_cost,
                            holding_costs=holding_costs,
                            delivery_cost=delivery_cost,
                            stock_out_cost=stock_out_cost,
                            demand=demand[sku],
                            policy_type=policy_types[sku])
                
                sim_results["SKU_"+str(sku)]["s_"+str(s*nr_sims + s1)] = output
                sim_config["SKU_"+str(sku)]["s_"+str(s*nr_sims + s1)] = {
                    "Simulation": (s*nr_sims + s1),
                    "Time Periods": time_periods,
                    "Max Quantity": max_quantities[sku],
                    "Review Period": review_periods[sku],
                    "Constant Quantity": constant_quantities[sku],
                    "Starting Inventory": starting_inventory[sku],
                    "ROP": rop[sku],
                    "Lead Time": lead_time_mean[sku%2],
                    "Policy Type":policy_types[sku] 
                }          

        else: 
            # run the simulation for continous review 
            output = funcs.inventory_sim(
                        time_periods=time_periods,
                        max_quantity=max_quantities[sku],
                        constant_quantity=constant_quantities[sku],
                        starting_inventory=starting_inventory[sku],
                        rop=rop[sku],
                        lead_time=lead_time_mean[sku%2],
                        per_item_cost=per_item_cost,
                        holding_costs=holding_costs,
                        delivery_cost=delivery_cost,
                        stock_out_cost=stock_out_cost,
                        demand=demand[sku],
                        policy_type=policy_types[sku])
        
            sim_results["SKU_"+str(sku)]["s_"+str(s)] = output
            sim_config["SKU_"+str(sku)]["s_"+str(s)] = {
                    "Simulation": s,
                    "Time Periods": time_periods,
                    "Max Quantity": max_quantities[sku],
                    "Review Period": review_periods[sku],
                    "Constant Quantity": constant_quantities[sku],
                    "Starting Inventory": starting_inventory[sku],
                    "ROP": rop[sku],
                    "Lead Time": lead_time_mean[sku%2],
                    "Policy Type":policy_types[sku] 
                }   


df_output = pd.DataFrame() # simulation results will go here
df_config = pd.DataFrame() # simulation configuration data will go here

# convert the nested results and config dicionaries into dataframes
for key in sim_results.keys():
    df_c = pd.DataFrame.from_dict(sim_config[key],orient='index')
    df_c["SKU"] = key
    df_config = pd.concat([df_config, df_c])
    
    for sub_key in sim_results[key].keys():

        df = pd.DataFrame.from_dict(sim_results[key][sub_key],orient='index')
        df["Simulation"] = sub_key
        df["SKU"] = key
        df_output = pd.concat([df_output, df])

df_output.to_csv('data/sim_results.csv', index=False)
df_config.to_csv('data/sim_config.csv', index=False)

