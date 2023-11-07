from abc import ABC, abstractmethod
import numpy as np
import pandas as pd
import random

class DemandInterface(ABC):
    
    @abstractmethod
    def generate(self) -> None:
        pass


class Demand_Random(DemandInterface):
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


class Demand_Trend(DemandInterface):
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


class Demand_Seasonal(DemandInterface):
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



class Demand_Gen():
    

    def __init__(self, weeks) -> None:
        self.period = weeks
        
        
    def generate(self, type) -> None:
        
        if type == 'random':
            return Demand_Random().generate(weeks=self.period)

        elif type == 'trend':
            return Demand_Trend.generate(weeks=self.period)
        
        elif type == 'seasonal':
            return Demand_Seasonal().generate(weeks=self.period)
        
        else: 
            raise ValueError('Invalid demand type')


weekss=50
test = Demand_Gen(weeks=weekss).generate(type='seasonal')

print(test)




