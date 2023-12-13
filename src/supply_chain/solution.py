import random
import numpy as np
import pandas as pd
import GA_core as ga_opt
import supply_chain as sc

class Individual_Solution(ga_opt.Chromosome):
    """A class representing an inidividual solution (i.e., a collection of policies)

    Attributes:
        skus (list): a list of SKU_Type objects 
    """

    def __init__(self) -> None:
        """A constructor for the Individual_Solution class.

        """
        self.solution = []
        
        
    def solution_initialize(self,
                            skus: list) -> None:

        """Initialise the solution
        
        Args:
            skus (list): a list of SKU_Type objects 
        """
       
        policy_factory = sc.Policy_Factory()

        for sku in skus:
            # select a random policy type
            policy_type = random.choice(policy_factory.options)
            # create a policy
            policy = policy_factory.create_policy(policy_type, sku)
            # add to the solution
            self.solution.append(policy)


    def solution_update(self, 
                        value: list) -> None:
        """Update solution attribute

        Args:
            value (list): a list of policy objects
        """
        if len(self.solution) != len(value):
            ValueError("The new solution must be of the same length as the old solution.") 

        self.solution = value


    def solution_evaluation(self,
                    demand: pd.DataFrame,
                    time_periods: int,
                    lead_time: int = 2,
                    stockout_coeff: float = 1.5,
                    holding_cost: float = 10.5) -> float:

        """Evaluate the fitness of the solution

            FF = Order Costs + Holding Costs + Stockout Costs 

        Returns:
            float: the fitness of the solution
        """
        nr_skus = demand.shape[0]

        holding_costs = np.zeros((nr_skus, time_periods))
        stockout_costs = np.zeros((nr_skus, time_periods))
        order_costs = np.zeros((nr_skus, time_periods))

        invenotry = np.zeros((nr_skus, time_periods))
        orders = np.zeros((nr_skus, time_periods))

        for t in range(time_periods):
            demand_t = demand['week_' + str(t)]

            for i, sku_d in enumerate(demand_t):
                policy = self.solution[i]
                per_item_cost = policy.sku.per_item_cost

                # quantity on hand (invetory[t])
                qoh = invenotry[i][t] if t != 0 else policy.sku.quantity
                # quantity on order    
                qoo = 0 if t <= lead_time else np.sum(orders[i][t-lead_time:t])
                
                # an order needs to be placed and the order wil be delivered before the end of the time period
                if policy.check_if_order_needed(qoh=qoh, on_order=qoo, period=t) == True and (t + lead_time) < time_periods:

                    order_q = policy.order_quantity(qoh=qoh, on_order=qoo)
                    # update orders
                    orders[i][t+lead_time] = order_q
                    # update order costs
                    order_costs[i][t] = order_q * per_item_cost
                
                # update inventory[t+1]
                if t < time_periods-1:
                    invenotry[i][t+1] = qoh + orders[i][t] - sku_d
                # update holding costs
                holding_costs[i][t] = qoh * holding_cost if qoh > 0 else 0
                # update stockout costs
                stockout_costs[i][t] = qoh * per_item_cost * stockout_coeff if qoh < 0 else 0


        np.savetxt('inventory.csv', invenotry, delimiter=',', fmt='%.0f')
        np.savetxt('orders.csv', orders, delimiter=',', fmt='%.0f')
        np.savetxt('holding_costs.csv', holding_costs, delimiter=',', fmt='%.2f')
        np.savetxt('stockout_costs.csv', stockout_costs, delimiter=',', fmt='%.2f')
        np.savetxt('order_costs.csv', order_costs, delimiter=',', fmt='%.2f')

        # find fitness
        fitness = np.sum(order_costs) + np.sum(holding_costs) + np.sum(stockout_costs)

        return fitness



    def mutate_chrom(self,
               loc: int) -> None:
        
        """Mutates a policy in the solution

        Args:
            loc (int): location of the mutation
        """

        gene = self.solution[loc]
        gene.mutate_gene()