from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import random

class Demand(ABC):
    """A class representing the demand interface.

    Args:
        ABC (class): Abstract class
    """
    
    @abstractmethod
    def generate(self) -> None:
        """Placeholder method for demand generation.
        """
        pass


class Demand_Random(Demand):
    """A class used to represent random demand.

    Args:
        DemandInterface (class): Abstract parent class
    """
    
    def generate(self,
                 weeks = 50) -> list:
        """Generates random demand.  

        Args:
            weeks (int, optional): the number of data points in the demand list. Defaults to 50.

        Returns:
            list: a list of integers representing random demand
        """
        
        trend = [random.uniform(1.0, 3) for _ in range(weeks)]
        seasonality = [random.uniform(0.8, 1.2) for _ in range(weeks)]  
        
        return [int(100 * trend[i] * seasonality[i]) for i in range(weeks)]


class Demand_Trend(Demand):
    """A class used to represent demand with a trend.

    Args:
        DemandInterface (class): Abstract parent class
    """
    
    def generate(self,
                 weeks = 50, 
                 trend_coeff=0.1) -> list:
        """Generates demand with a trend.  

        Args:
            weeks (int, optional): the number of data points in the demand list. Defaults to 50.
            trend_coeff (float, optional): a coefficient to adjust the slope of the trend. Defaults to 0.1.    

        Returns:
            list: a list of integers representing demand with a trend.
        """
        
        trend = [random.uniform(1.0, 3) + trend_coeff*x for x in range(weeks)]
        seasonality = [random.uniform(0.8, 1.2) for _ in range(weeks)]  
        
        return [int(100 * trend[i] * seasonality[i]) for i in range(weeks)]


class Demand_Seasonal(Demand):
    """A class used to represent seasonal demand.

    Args:
        DemandInterface (class): Abstract parent class
    """
    
    def generate(self, 
                 weeks = 50,
                 freq_coeff=0.2) -> list:
        """Generates seasonal demand. 

        Args:
            weeks (int, optional): the number of data points in the demand list. Defaults to 50.
            freq_coeff (float, optional): a coefficient to adjust the frequency of the seasonality. Defaults to 0.2.

        Returns:
            list: a list of integers representing seasonal demand.
        """
        
        trend = [random.uniform(1.0, 3) for _ in range(weeks)]
        seasonality = [np.sin(freq_coeff*x) + 1 for x in range(weeks)]  
        
        return [int(100 * trend[i] * seasonality[i]) for i in range(weeks)]



class Demand_Factory():
    """A class implementing the factory design pattern.
    """
    

    def __init__(self, 
                 weeks:int) -> None:
        """A constructor for the Demand_Gen class.

        Args:
            weeks (int): the number of weeks demand must be generated for.
        """
        self.period = weeks
        
        
    def generate(self,
                 nr_skus:int,
                 split:list, 
                 type:list) -> pd.DataFrame:
        """Generated demand according to the type specified.

        Args:
            nr_skus (int): the number of items
            split (list): the split of items across the policies 
            type (list): policy type for each split

        Raises:
            ValueError: raises an error if invalid demand type is provided

        Returns:
            pd.Dataframe: a dataframe with a column per time period and a row per sku + a column for sku names
        """
        
        # check the dimension match 
        if len(split) != len(type):
            raise ValueError("The number of splits does not match the number of policy types")
        
        # check the splits sum up to the total number of skus
        if sum(split) != nr_skus:
            raise ValueError("The split do not sum up to the total number of SKUs")
        
        columns = ['week_' + str(x) for x in range(self.period)]  # column headers      
        data = [] # demands will go here

        for i, demand in enumerate(type):
            if demand == 'random':
                for _ in range(split[i]):
                    data.append(Demand_Random().generate(weeks=self.period))

            elif demand == 'trend':
                for _ in range(split[i]):
                    data.append(Demand_Trend.generate(weeks=self.period))
            
            elif demand == 'seasonal':
                for _ in range(split[i]):
                    data.append(Demand_Seasonal().generate(weeks=self.period))
            
            else: 
                raise ValueError('Invalid demand type')
        
        # creat a column for skus    
        skus = pd.DataFrame({'skus' : ['sku'+str(x) for x in range(nr_skus)]}) 
        # create a df for demands
        df_demand = pd.DataFrame(data=data, columns=columns)
        # combine the sku and demand dataframes
        df_demand = skus.join(df_demand)

        return df_demand




