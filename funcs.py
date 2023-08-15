import math
import random
import pandas as pd
import numpy as np
import scipy.stats as stats
from datetime import datetime

def generate_demand(
        nr_SKUs: int = 2,
        time_periods: int = 90,
        demand_mean: list = [random.randint(300, 600) for i in range(2)],
        demand_sd: list = [random.randint(50, 100) for i in range(2)]
) -> np.array: 
    
    """"
    The function generates a NumPy list for each SKU with a random daily demand (positive integers with normal distribution).

    Inputs: 
        nr_SKUs (int) - the number of SKUs a random demand will be generated for
        time_periods (int) - the number of dates to be generated 
        demand_mean (list) - mean of the generated demand
        demand_sd (list) - standard deviation of the generated mean

    Outputs: 
        Numpy array with dimensions (nr_SKUs, time_periods)
    """

    d = [] # demand generated for each SKU goes here

    # generate demand 
    for i in range(nr_SKUs):
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
        d: int, # either 0 or 1
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
    carry_over_costs = i * inventory * per_item_cost * holding_costs
    delivery_costs = d * (delivery_cost + per_item_cost * order_size)
    stock_out_costs = s * stock_out_cost
    
    total_cost = carry_over_costs + delivery_costs + stock_out_costs

    costs = {
        "Carryover Cost": carry_over_costs,
        "Delivery Cost": delivery_costs,
        "Stockout Costs": stock_out_costs,
        "Total Costs": total_cost
    }

    return costs
