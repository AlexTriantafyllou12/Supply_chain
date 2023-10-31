import Utility as u 
import random 

class Warehouse:
    def __init__(self,
                 max_capacity,
                 current_capacity,
                 maintenance_cost) -> None:
        
        self.max_capacity = max_capacity
        self.current_capacity = current_capacity
        self.maintenance_cost = maintenance_cost

    @u.check_integer_input
    def set_current_capacity(self, value) -> None:
        self.current_capacity = value

    def allocate_space(self, nr_skus) -> list:
        max_capacity = self.max_capacity
        allocations = [] # capacity allocation per SKU goes here

        # allocate capacity for the first n-1 items (out of n)
        for i in range(nr_skus-1):
            # find the allocation per item
            allocated_q = random.randint(1, max_capacity - nr_skus + i - 1)
            # ensure an item doesn't take up more than half the warehouse
            while allocated_q/max_capacity > 0.5:
                allocated_q = random.randint(1, max_capacity - nr_skus + i - 1)
            
            # update the maximum capacity
            max_capacity = max_capacity - allocated_q
            allocations.append(allocated_q)
        
        # allocate the leftover capacity to the final item
        allocations.append(max_capacity)
        return allocations
    
