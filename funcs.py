import types
import random
import pandas as pd
import numpy as np
from datetime import datetime


def generate_demand(
        nr_SKUs: int = 2,
        start_date: str = "2023-08-01",
        time_periods: int = 90
) -> pd.DataFrame: 
    
    """"
    The function generates a dataframe with a date column in the specified range and a column for each SKU with a random daily demand (positive integers with normal distribution).

    Inputs: 
        nr_SKUs (int) - the number of SKUs a random demand will be generated for
        start_date (str) - a date string in the format 'yyyy-mm-dd'
        time_periods (int) - the number of dates (days) to be generated 

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
    demand["date"] = pd.date_range(start_date, periods=time_periods, freq='D')

    return demand

