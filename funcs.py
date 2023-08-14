import random
import pandas as pd
import numpy as np
from datetime import datetime

def generate_demand(
        nr_SKUs: int = 2,
        start_date: str = "2023-08-01",
        time_periods: int = 90,
        freq: str = "D"
) -> pd.DataFrame: 
    
    """"
    The function generates a dataframe with a date column in the specified range and a column for each SKU with a random daily demand (positive integers with normal distribution).

    Inputs: 
        nr_SKUs (int) - the number of SKUs a random demand will be generated for
        start_date (str) - a date string in the format 'yyyy-mm-dd'
        time_periods (int) - the number of dates to be generated 
        freg (str) - frequency of the dates generated, see here of options: https://pandas.pydata.org/docs/user_guide/timeseries.html#offset-aliases

    Outputs: 
        Pandas datafrfame
    """
    d = {} # demand generated for each SKU goes here

    # generate the demand 
    for i in range(nr_SKUs):

        rand_demand = np.random.normal(
                                loc=random.randint(100, 500), 
                                scale=random.randint(10, 50), 
                                size=time_periods)
        
         # convert generated demand into positive integers
        positive_rand_demand = (abs(int(x)) for x in rand_demand)
        d['SKU_'+str(i)] = positive_rand_demand

    demand = pd.DataFrame(d)  
 
    # convert input date from string to date data typye
    start_date = datetime.strptime(start_date, "%Y-%m-%d")
    # add a date column to the dataframe
    demand["date"] = pd.date_range(start_date, periods=time_periods, freq=freq)

    return demand


def find_safety_stock(
        demand: list,
        max_lead_time: int = 7,
        avg_lead_time: int = 3
) -> int:
    
    """
    The function finds an item's safety stock (SS) following the formula:
    SS = (Max Daily Sales x Max Lead Time) - (Avg Daily Sales x Avg Lead Time)

    Input:
        demand (list) - a list of demand values over a given time period
        max_lead_time (int) - assumed max lead time (days) 
        avg_lead_time (int) - assumed average lead time (days)

    Output: 
        Safety stock (integer)
    """

    # find max and average demand values
    max_demand = max(demand)
    avg_demand = int(sum(demand) / len(demand))

    # calcualte the safety stock
    safety_stock = max_demand * max_lead_time - avg_demand * avg_lead_time

    return safety_stock

def find_reorder_point(
        demand: list,
        avg_lead_time: int = 3,
        safety_stock: int = 900
) -> int:
    
    """
    The function an SKU's reorder point (ROP) following the formula:
    ROP = (Lead Time x Demand Rate) + Safety Stock

    Input:
        demand (list)
        avg_lead_time (int)
        safety_stock (int)
    Returns:
        reorder_point (int)
    """
    # assume constant demand rate over the given time period
    avg_demand = int(sum(demand) / len(demand))
    # find the reorder point
    reorder_point = avg_lead_time*avg_demand + safety_stock

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
    
