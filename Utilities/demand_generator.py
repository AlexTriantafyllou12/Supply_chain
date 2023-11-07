import numpy as np
import pandas as pd
import random



random.seed(999)

weeks = 52


class DemandInterface:
    
    def generate(self) -> None:
        pass


class Demand_var1(DemandInterface):
    
    def generate(self) -> list:
        
        trend = [random.uniform(1.0, 3) for _ in range(weeks)]
        seasonality = [random.uniform(0.8, 1.2) for _ in range(weeks)]  
        
        return [int(100 * trend[i] * seasonality[i]) for i in range(weeks)]




class Demand_Gen():
    

    def __init__(self, weeks) -> None:
        self.period = weeks
        
        
    @staticmethod
    def generate(type) -> None:
        
        if type == '1':
            return Demand_var1().generate()




test = Demand_Gen(weeks=weeks).generate(type='1')

print(test)




