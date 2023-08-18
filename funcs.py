import math
import random
import pandas as pd
import numpy as np
import scipy.stats as stats
from datetime import datetime

def generate_demand(
        nr_SKUs: int = 1,
        time_periods: int = 90,
        frequency: int = [1],
        distribution_type: list = ["norm"],
        demand_mean: list = [random.randint(300, 600) for i in range(2)],
        demand_sd: list = [random.randint(50, 100) for i in range(2)]
) -> np.array: 
    
    """"
    The function generates a NumPy list for each SKU with a random daily demand with the given distribution and frequency (e.g., daily, weekly).

    Inputs: 
        nr_SKUs (int) - the number of SKUs a random demand will be generated for
        time_periods (int) - the number of dates to be generated 
        frequency (int) - demand frequency, e.g., 1 = daily, 7 = weekly, 30 = monthly etc
        distribution_type (str) - options include "norm", "poisson" and "binomial"
        demand_mean (list) - mean of the generated demand
        demand_sd (list) - standard deviation of the generated mean

    Outputs: 
        Numpy array with dimensions (nr_SKUs, time_periods)
    """

    d = [] # demand generated for each SKU goes here

    # generate demand 
    for i in range(nr_SKUs):

        match distribution_type[i]:
            case "norm":
                rand_demand = np.random.normal(
                                        loc=demand_mean[i], 
                                        scale=demand_sd[i], 
                                        size=time_periods)
                # convert into integers
                rand_demand = rand_demand.astype(int)
                # check for negative numbers     
                min_demand = np.min(rand_demand)
                # if the distribution has a negative value, shift the whole dataset to the right
                if min_demand < 0:
                    rand_demand = rand_demand - 2 * min_demand
                    
            case "poisson":
                rand_demand = np.random.poisson(
                                        lam=demand_mean[i], 
                                        size=time_periods)
            
            case "binomial":
                rand_demand = np.random.binomial(
                                        n=2,
                                        p=0.15,
                                        size=time_periods)
                # scale the binomial distribution
                rand_demand = np.array([demand_mean[i] + j*demand_sd[i] for j in rand_demand])
        
        # adjust demand frequency     
        if frequency[i] > 1:
            for j in range(time_periods):
                if j%frequency[i] != 0:
                    rand_demand[j] = 0
    
        d.append(rand_demand)

    demand = np.asarray(d) # convert into a numpy array 

    return demand


def find_safety_stock(
        demand_mean: int =random.randint(100, 500),
        demand_sd: int = random.randint(10, 50),
        lead_time_mean: int = random.randint(1, 4),
        lead_time_sd: int = random.randint(1, 3),
        CSL: float = 0.999
) -> int:
    
    """
    The function finds an item's safety stock (SS) following the formula:
    SS = k * (Lead Time * SD_demand^2 + Demand * SD_lead_time^2)^0.5
    where k is calculated using a target metric (e.g. CSL)

    Output: 
        Safety stock (integer)
    """

    # find k given a CSL target
    k = round(stats.norm(0, 1).ppf(CSL),2)

    # find the reorder point
    safety_stock = int(k * math.sqrt(lead_time_mean*(demand_mean**2) + demand_mean*(lead_time_sd**2)))
    print("With average demand {}, SD_demand of {}, average lead time {} and SD_lead_time of {}, the value of k is {} and safety stock is {}".format(demand_mean, demand_sd, lead_time_mean, lead_time_sd, k, safety_stock))

    return safety_stock

def find_reorder_point(
        demand_mean: int,
        safety_stock: int,
        lead_time_mean: int
) -> int:
    
    """
    The function an SKU's reorder point (ROP) following the formula:
    ROP = (Lead Time x Demand Rate) + Safety Stock

    Returns:
        reorder_point (int)
    """

    # find the reorder point
    reorder_point = lead_time_mean*demand_mean + safety_stock

    return reorder_point


def generate_inventory(
        demand: list, 
        reorder_point: int,
        max_capacity: int = 5000
) -> list:
    
    """
    The function generates inventory levels given demand and maximum inventory capacity.

    Input:
        demand (list)
        reorder_point (int)
        max_capacity (int)

    Returns:
        inventory_list (list)
    """
    inventory_list = [] # daily inventory levels go here
    inv = max_capacity # assume inventory is at full capacity at the beginning of the given time period
    
    # find the daily inventory level
    for i in range(len(demand)):
        # inventory left after fulfilling demand
        inventory_left  = inv-demand[i]
        inventory_list.append(inventory_left)
        # if inventory left is above the reorder point, do not restock
        if reorder_point < inventory_left:
            inv = inventory_left
        # if inventory left is below the reorder point, restock
        else:
            inv = max_capacity

    return inventory_list

# cost_func_t = i * inventory_t-1 * per_item_cost * holding_costs + d * delivery_cost + s * stock_out_cost
def cost_function(
        i: int, # either 0 or 1 
        inventory: int,
        per_item_cost: int, 
        holding_costs: float,
        d1: int, # either 0 or 1
        d2: int, # either 0 or 1
        delivery_cost: int,
        order_size: int,
        s: int, # either 0 or 1
        stock_out_cost: int          
) -> dict:
    
    """
    The function calculates the total inventory costs following a formula:
        cost_func_t = i * inventory_t-1 * per_item_cost * holding_costs + d * (delivery_cost + order_size * per_itme_cost) + s * stock_out_cost
    Variables i, d and s will have a value of 1 or 0 to indicate if the argument is applicable in the cost function. 

    Returns:
        cost_func (float)
    """
    carry_over_costs = i * inventory * holding_costs
    delivery_costs = d1 * delivery_cost + d2 * per_item_cost * order_size
    stock_out_costs = s * stock_out_cost
    
    total_cost = carry_over_costs + delivery_costs + stock_out_costs

    costs = {
        "Carryover Cost": carry_over_costs,
        "Delivery Cost": delivery_costs,
        "Stockout Costs": stock_out_costs,
        "Total Costs": total_cost
    }

    return costs


def inventory_sim(
        simulations: int,
        time_periods: int,
        nr_SKUs: int,
        nr_suppliers: int,
        starting_inventory: list,
        rop: list,
        delivery_cost: int,
        per_item_cost: int,
        holding_costs: float,
        stock_out_cost: int,
        demand: list,
        lead_time: list = np.arange(2, 14, 1),
        review_period: list = np.arange(2, 30, 1),
        max_quantity: list = np.arange(4000, 20000, 500),

) -> dict:
    
    """
    The function runs a simulation of an SKU inventory given some demand and assuming the specified policy.

    Returns:
        sim_results (dict) - a nested dictionary 
    """
    
    sim_results = {} # simulation results
    sim_config = {} # simulation configuration
 
   # randomly assign SKUs to suppliers
    SKUs_per_supplier = [[] for sup in range(2)]
    SKUs = np.arange(0,nr_SKUs,1)
    random.shuffle(SKUs)
    while len(SKUs) > 0:
        for sup in range(nr_suppliers):
            if (len(SKUs) > 0):
                SKUs_per_supplier[sup].append(SKUs[0])
                SKUs = np.delete(SKUs, [0])

    for supplier in range(nr_suppliers):  
        
        sim_results["sup_"+str(supplier)] = {}
        sim_config["sup_"+str(supplier)] = {}      
    
        for s0 in range(simulations):
            # delivery arrival time period and size, there might be several deliveries in the pipeline, hence a list is used
            t_arrival = []
            delivery_size = []
            policy_types = ["periodic", "continuous"]
            # select a policy per SKU
            sku_policies = [policy_types[np.random.randint(0,2)] for i in range(nr_SKUs)]
            # select max quantity per sku
            sku_max_quantities = [random.choice(max_quantity) for i in range(nr_SKUs)]

            for i in range(nr_SKUs):
                t_arrival.append([])
                delivery_size.append([])
            
            for s1 in range(simulations):
                inventory = starting_inventory.copy()
                sku_review_period = []
                # find a random review period for SKUs with periodic review policy
                for j in range(nr_SKUs):
                    if sku_policies[j] == policy_types[0]:
                        sku_review_period.append(random.choice(review_period))
                    else:
                        sku_review_period.append(1)
                
                sim_results["sup_"+str(supplier)]["s_" + str(s0*simulations + s1)] = {}
                sim_config["sup_"+str(supplier)]["s_" + str(s0*simulations + s1)] = {}
                
                for t in range(time_periods):

                    sim_results["sup_"+str(supplier)]["s_" + str(s0*simulations + s1)]["t_" + str(t)] = {}
                    sim_config["sup_"+str(supplier)]["s_" + str(s0*simulations + s1)]["t_" + str(t)] = {}
                    
                    already_ordered = False
                    order_lead_time = 0
                    
                    for sku in SKUs_per_supplier[supplier]:
                        d1 = 0
                        d2 = 0
                        s = 0
                        i = 1
                        sku_cost = 0
                        order = 0 # order size 
                        
                        # is it review day?
                        if t%sku_review_period[sku] == 0:

                            # reorder if inventory below ROP
                            if inventory[sku] < rop[sku]:

                                d1 = 0 if already_ordered else 1 # check if delivery costs need to be accounted for
                                d2 = 1 # indicate an order took place
            
                                # find order size
                                order = sku_max_quantities[sku] - inventory[sku]
                                
                                if not already_ordered:
                                    order_lead_time = random.choice(lead_time)
                                    already_ordered = True
    
                                t_arrival[sku].append(t + order_lead_time) # order arrival time period
                                delivery_size[sku].append(order) 

                                                        # find delivery cost respective or order size items
                                for c in per_item_cost[sku]:
                                    if order in range(c[0], c[1]):
                                        sku_cost = c[2]
                                        break

                        # has there been a stock out?
                        if inventory[sku] < 0:
                                s = 1 # indicate there was a stock out
                                i = 0 # indicate there's no stock

                        # find the cost 
                        cost = cost_function(
                                                i=i, 
                                                inventory=inventory[sku],
                                                per_item_cost=sku_cost,
                                                holding_costs=holding_costs,
                                                d1=d1,
                                                d2=d2,
                                                order_size=order,
                                                delivery_cost=delivery_cost,
                                                s=s,
                                                stock_out_cost=stock_out_cost)
            
                        # save the results 
                        # inventory is recorded at the beginning of the day (following a delivery (if any)) 
                        # demand_t will affect inventory_t+1
                        sim_results["sup_"+str(supplier)]["s_" + str(s0*simulations + s1)]["t_" + str(t)]["sku_"+str(sku)] = {
                            "SKU": sku,
                            "Period": t,
                            "Simulation": (s0*simulations + s1),
                            "Supplier": supplier,
                            "Demand": demand[sku][t],
                            "Inventory": inventory[sku],
                            "Ordered": order,
                            "Lead Time": order_lead_time,
                            "Carryover Cost": cost["Carryover Cost"],
                            "Delivery Cost": cost["Delivery Cost"],
                            "Stockout Costs": cost["Stockout Costs"],
                            "Total Costs": cost["Total Costs"],
                        }
                        if t == 0:
                            sim_config["sup_"+str(supplier)]["s_" + str(s0*simulations + s1)]["sku_"+str(sku)]  = {
                                "Simulation": (s0*simulations + s1),
                                "SKU": sku,
                                "Time Periods": time_periods,
                                "Max Quantity": sku_max_quantities[sku],
                                "Review Period": sku_review_period[sku],
                                "Starting Inventory": starting_inventory[sku],
                                "ROP": rop[sku],
                                "Lead Time": order_lead_time,
                                "Policy Type":sku_policies[sku] 
                            }  
            
                        # find next day's inventory
                        # is it delivery day?
                        if t in t_arrival[sku]:    
                            while t in t_arrival[sku]:
                                index = t_arrival[sku].index(t)
                                inventory[sku] = inventory[sku] - demand[sku][t] + delivery_size[sku][index]
                                # remove from the list 
                                t_arrival[sku].pop(index)
                                delivery_size[sku].pop(index)
                        
                        else:
                            inventory[sku] = inventory[sku] - demand[sku][t]

    return sim_results, sim_config




