import math
import random
import numpy as np
import Utility as u
import scipy.stats as stats

class SKUType:

    starting_inventory = random.randint(100, 500)

    def __init__(self,
                 name,
                 holding_cost,
                 actual_invenotry=starting_inventory,
                 estimated_invenotry=starting_inventory, 
                 demand=None,
                 policy_type=None,
                 review_period=1, 
                 max_quantity=None,
                 rop=None, 
                 lead_time_mean=random.randint(1, 5),
                 lead_time_sd=random.randint(1, 3),
                 demand_mean = random.randint(100, 500),
                 demand_sd = random.randint(10, 50)) -> None:
        
        self.name = name
        self.holding_cost = holding_cost
        self.actual_invenotry = actual_invenotry
        self.estimated_invenotry = estimated_invenotry
        self.demand = demand
        self.policy_type = policy_type
        self.review_period = review_period
        self.max_quantity = max_quantity
        self.rop = rop
        self.lead_time_mean = lead_time_mean
        self.lead_time_sd = lead_time_sd
        self.demand_mean = demand_mean
        self.demand_sd = demand_sd  
  
    def set_policy(self, value) -> None:
        if value not in ("periodic", "continous"):
            raise ValueError("Expected 'periodic' or 'continous' value")
        
        self.policy_type = value

        # automatically set the review period for continous policies to every day
        if value == "continous":
            self.set_review_period(1) 
    

    @u.check_integer_input
    def set_review_period(self, value) -> None:
        if self.policy_type == "continous" and value != 1:
            raise ValueError("Review period must be 1 for continous policies")
        
        self.review_period = value
    
    @u.check_integer_input
    def set_max_quantity(self, value) -> None:
        self.max_quantity = value

    @u.check_integer_input
    def set_actual_inventory(self, value) -> None:
        self.actual_invenotry = value

    @u.check_integer_input
    def set_estimated_invenotry(self, value) -> None:
        self.estimated_invenotry = value    

    def set_demand(self, value) -> None:
        self.demand = value

    @u.check_integer_input
    def set_rop(self, value) -> None:
        self.rop = value

  
    def find_rop(self,
                CSL: float = 0.999) -> int:
            
            """
            The function finds an SKU's reorder point (ROP) following the formula:
            ROP = (Lead Time x Demand Rate) + Safety Stock

            An item's safety stock (SS) is calculated following the formula:
            SS = k * (Lead Time * SD_demand^2 + Demand * SD_lead_time^2)^0.5
            where k is calculated using a target metric (e.g. CSL)

            Returns:
                reorder_point (int)
            """

            # find k given a CSL target
            k = round(stats.norm(0, 1).ppf(CSL),2)

            # find the safety stock
            safety_stock = int(k * math.sqrt(self.lead_time_mean*(self.demand_sd**2) + self.demand_mean * (self.lead_time_sd**2)))

            # find the reorder point
            reorder_point = self.lead_time_mean*self.demand_mean + safety_stock

            if isinstance(self.max_quantity, int) and reorder_point > self.max_quantity:
                raise Exception("Reordering point is larger than the maximum quantity of the SKU stored.")

            return reorder_point


    def find_quantity_to_order(self, current_day) -> int:

        """
        The function finds an item's quantity to order (QTO) based on the following formula:
        QTO = Max Quantity - Actual Invenotry - Upcoming Demand

        Returns:
            quantity_to_order (int)
        """
        
        upcoming_demand = 0
        for i in range(self.lead_time_mean):
            upcoming_demand += self.demand[current_day]
            current_day += 1

        quantity_to_order = self.max_quantity - self.actual_invenotry - upcoming_demand

        return quantity_to_order


    def generate_demand(self,
                        time_periods: int=90,
                        frequency: int=1,
                        distribution_type: str="norm") -> np.array:
        
        if distribution_type not in ("norm", "poisson", "binomial"):
            raise ValueError("distribution_type: Expected a value 'norm', 'poisson' or 'binomial")

        rand_demand = []

        match distribution_type:
            case "norm":
                rand_demand = np.random.normal(
                                        loc=self.demand_mean, 
                                        scale=self.demand_sd, 
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
                                        lam=self.demand_mean, 
                                        size=time_periods)
            
            case "binomial":
                rand_demand = np.random.binomial(
                                        n=2,
                                        p=0.15,
                                        size=time_periods)
                # scale the binomial distribution
                rand_demand = np.array([self.demand_mean + j*self.demand_sd for j in rand_demand])
        
        # adjust demand frequency     
        if frequency > 1:
            for j in range(time_periods):
                if j%frequency != 0:
                    rand_demand[j] = 0

        return rand_demand