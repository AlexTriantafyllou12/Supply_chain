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
            rop=sku.rop
            # ensure rop does not exceed the max quantity for the SKU
            while rop is None or rop > sku.max_quantity:
                rop =sku.find_rop()
                print(rop)
            
            sku.set_rop(rop)
            
            meta_data.append([sku.rop, sku.max_quantity, sku.review_period])

            print('SKU: {}, ROP: {}, Max_q: {}, Lead_time {}'.format(sku.name, sku.rop, sku.max_quantity, sku.lead_time_mean))
         

        solution = []
        orders = []

        for p in range(self.nr_periods-1):
            
            solution.append([])
            to_be_ordered = []

            # check for deliveries 
            for ord in orders:
                if ord.delivery_day == p:

                    for sk_i, sk in enumerate(ord.SKUs):
                        sk.set_actual_inventory(ord.quantity[sk_i])

            for s_i, s in enumerate(skus):
                qantity_to_order = 0

                # is it review day?
                if p % s.review_period == 0:
                    
                    # is estimated inventory below ROP?
                    if s.rop < s.estimated_inventory:
                        
                        # how much stock will be required to fullfill demnad before the order arrives?
                        upcoming_demand = sum(s.demand[p:(p + s.lead_time_mean + 1)])

                        qantity_to_order = s.max_quantity - s.estimated_inventory + upcoming_demand 
                        # ensure the quantity ordered doesn't exceed max quantity 
                        qantity_to_order = qantity_to_order if qantity_to_order < s.max_quantity else s.max_quantity

                        to_be_ordered.append([s, qantity_to_order])
                        # update the estimated inventory
                        s.set_estimated_inventory(s.estimated_inventory + qantity_to_order)
                    
                    else:
                        to_be_ordered.append([s, 0])

                solution[p].append([s.actual_inventory, qantity_to_order])
                
                daily_demand = s.demand[p]
                s.set_estimated_inventory(int(s.estimated_inventory - daily_demand))
                s.set_actual_inventory(int(s.actual_inventory - daily_demand))

            # assign items to suppliers and place orders
            # randomly shuffle suppliers 
            random.shuffle(suppliers)

            for supplier in suppliers:
                items = []
                quantities = []
                prices = []

                for o_i, o in enumerate(to_be_ordered):
                    item = o[0]
                    quantity = o[1]
                    item_price = 0
                    item_supplied_by = 0

                    if quantity != 0:
                        item_price  = supplier.find_sku_price(item.name, quantity)

                        # assign item if it's delivered by the supplier
                        if item_price != 0:
                            item_supplied_by = supplier.name 
                            items.append(item)
                            quantities.append(quantity)
                            prices.append(item_price)

                            to_be_ordered.pop(o_i)

                    new_order = Order.Order(items, quantities, prices, supplier.delivery_cost, p+supplier.lead_time)
                    orders.append(new_order)

                    solution[p][o_i].append(item_supplied_by)
                    solution[p][o_i].append(item_price)

        return meta_data, solution



