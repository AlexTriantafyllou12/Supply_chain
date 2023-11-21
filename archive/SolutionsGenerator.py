import numpy as np
import Warehouse
import SKUType
import Supplier
import Order
import random

class SolutionGenerator:
    def __init__(self,
                 nr_periods,
                 nr_skus
                 ) -> None:
        
        self.nr_periods = nr_periods
        self.nr_skus = nr_skus

    def generate_random_solution(self,
                                  skus: list, 
                                  suppliers: list,
                                  warehouse: Warehouse # how to account for multiple warehouses?
                                 ) -> list:
        
        """The method generates a random solution for an invenotry plan.

        Returns:
            meta_data: a nested list with details about the ROP, maximum quantity and review period per SKU.
            solution: a nested list with details about the actual invenotry, quantity ordered, supplier name and price per time period and SKU.
        """
        
        meta_data = [] # ROPs and max quantities per SKU will go here

        review_periods = np.arange(1, 30, 1)
        
        # allocate warehouse space per sku
        space_allocations = warehouse.allocate_space(self.nr_skus)
        print("Before SKUs")
        for i, sku in enumerate(skus):
            # set the max quantity based on warehouse allocation
            sku.set_max_quantity(space_allocations[i])
            # set a random review period
            sku.set_review_period(random.choice(review_periods))
            rop=sku.find_rop()
            sku.set_rop(rop)
            # ensure rop does not exceed the max quantity for the SKU
            if rop > sku.max_quantity:
                sku.set_rop(int(sku.max_quantity/2))
            
            meta_data.append([sku.rop, sku.max_quantity, sku.review_period])

            print('SKU: {}, ROP: {}, Max_q: {}, Lead_time {}, Review Period {}'.format(sku.name, sku.rop, sku.max_quantity, sku.lead_time_mean, sku.review_period))
         
        solution = []
        orders = []

        for p in range(self.nr_periods-1):
            
            solution.append([])
            to_be_ordered = []

            # check for deliveries 
            for ord_i, ord in enumerate(orders):
                if ord.delivery_day == p:

                    for sk_i, sk in enumerate(ord.SKUs):
                        actual_invenotry = sk.actual_inventory + ord.quantity[sk_i]
                        sk.set_actual_inventory(actual_invenotry if actual_invenotry <= sk.max_quantity else sk.max_quantity)
                    
                    # remove the delivered order from the list
                    orders.pop(ord_i)

            for s_i, s in enumerate(skus):
                qantity_to_order = 0

                # is it review day?
                if p % s.review_period == 0:
                    
                    # is estimated inventory below ROP?
                    if s.rop > s.estimated_inventory:
                        
                        # how much stock will be required to fullfill demnad before the order arrives?
                        upcoming_demand = sum(s.demand[p:(p + s.lead_time_mean + 1)])

                        qantity_to_order = s.max_quantity - s.estimated_inventory + upcoming_demand 
                        # ensure the quantity ordered doesn't exceed max quantity 
                        qantity_to_order = qantity_to_order if qantity_to_order < s.max_quantity else s.max_quantity

                        # update the estimated inventory
                        s.set_estimated_inventory(s.estimated_inventory + qantity_to_order)           
                
                to_be_ordered.append([s_i, s, qantity_to_order])

                solution[p].append([s.actual_inventory, qantity_to_order])
                
                # account for the daily demand
                daily_demand = s.demand[p]
                estimated_inventory= int(s.estimated_inventory - daily_demand)
                actual_invenotry = int(s.actual_inventory - daily_demand)
                # ensure negative values are not passed in case of a stockout
                s.set_estimated_inventory(estimated_inventory if estimated_inventory >= 0 else 0)
                s.set_actual_inventory(actual_invenotry if actual_invenotry >= 0 else 0)

            # assign items to suppliers and place orders
            # randomly shuffle suppliers 
            random.shuffle(suppliers)
            already_ordered = [] # items already ordered from one of the suppliers go here

            for supplier in suppliers:
                items = [] # items to be ordered from the suppliers go here
                quantities = [] # quanities to be ordered go here
                prices = [] # price per item go here
       
                for o in to_be_ordered:

                    item = o[1]
                    quantity = o[2]
                    item_price = 0
                    item_supplied_by = 0

                    if item not in already_ordered: 
                        if quantity != 0:       
                            item_price  = supplier.find_sku_price(item.name, quantity)

                            # assign item if it's delivered by the supplier
                            if item_price != 0:
                                item_supplied_by = supplier.name 
                                items.append(item)
                                quantities.append(quantity)
                                prices.append(item_price)
                                
                        already_ordered.append(item)

                        solution[p][o[0]].append(item_supplied_by)
                        solution[p][o[0]].append(item_price)
                
                # place an order with the supplier
                new_order = Order.Order(items, quantities, prices, supplier.delivery_cost, p+supplier.lead_time)
                orders.append(new_order)
                        

        return meta_data, solution



