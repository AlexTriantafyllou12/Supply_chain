import funcs
import random
import numpy as np
import json

# define the restrictions
lead_time_mean  = [3, 5]
lead_time_sd    = [2, 1]

nr_SKUs         = 1
nr_sims         = 3

demand_mean     = [random.randint(300, 600) for i in range(nr_SKUs)]
demand_sd       = [random.randint(50, 100) for i in range(nr_SKUs)]

holding_costs   = 0.05 # percent of the total cost of the item stored
delivery_cost   = 100 # constant per delivery
stock_out_cost  = 100000
per_item_cost   = 100
time_periods    = 20
scrap_value     = 300

sim_results     = {} # simulation results will go here

# generate demand per SKU
demand = funcs.generate_demand(
    nr_SKUs=nr_SKUs,
    time_periods=time_periods,
    demand_mean=demand_mean,
    demand_sd=demand_sd
)

safety_stocks = np.asarray([funcs.find_safety_stock( 
                          demand_mean=demand_mean[i],
                          demand_sd=demand_sd[i],
                          lead_time_mean=lead_time_mean[i%2], # even SKUs delivered by suppplier 1 (index = 0), odd SKUs delivered by supplier 2 (index = 1)
                          lead_time_sd=lead_time_sd[i%2]  
                        ) for i in range(nr_SKUs)])

#print("SS: ", safety_stocks)

rop = np.asarray([funcs.find_reorder_point(
                    demand_mean=demand_mean[i],
                    safety_stock=safety_stocks[i],
                    lead_time_mean=lead_time_mean[i%2]
                    ) for i in range(nr_SKUs)])

print("ROP: ", rop)

# assume starting inventory is 3 times the reorder point
starting_inventory = np.asarray([rop[i] * 3 for i in range(nr_SKUs)])

# sampling population for the periodic review policy
periodic_review_periods = np.arange(1,90,1)

# sampling population for the 'order up to a point' policy
max_quantity = np.arange(4000, 20000, 500)

# sampling population for the 'constant quantity' policy
contant_quantity = np.arange(500, 20000, 500)

#for sample_inventory_policies:
 # SKU0 = periodic 5 day review, order up to a point
 # SKU1 = reorder once inventory levels reach reorder point (rop), constant quantity
 # SKU2 = reorder once inventory levels reach rop, order up to a point
 # SKU3 = reorder once inventory levels reach rop, constant quantity
 # SKU4 = periodic review, order up to 10000 units

inventory = starting_inventory
sku_0_review_days  = 2
sku_4_max_quantity = 10000

for s in range(nr_sims):
    sim_results["s_" + str(s)] = {} # results for each simulation will go here
    
    # define the review policy for each SKU
    max_quantity_SKU_0      = random.choice(max_quantity)
    constant_quantity_SKU_1 = random.choice(contant_quantity)
    max_quantity_SKU_2      = random.choice(max_quantity)
    contant_quantity_SKU_3  = random.choice(contant_quantity)
    periodic_review_SKU_4   = random.choice(periodic_review_periods)

    # delivery arrival time period and size, there might be several deliveries in the pipeline, hence a list is used
    t_arrival_0 = []
    replenishment_0 = []

    for t in range(time_periods):

        sim_results["s_" + str(s)]["t_" + str(t)] = {} # results for each time period will go here    
                
        # SKU0
        d_0 = 0
        s_0 = 0
        i_0 = 1
        order_0 = 0 # order size 
        current_inventory_0 = inventory[0]

        print("Tarrival: {}, t: {}".format(t_arrival_0, t))
        print("Replenishment ", replenishment_0)
        # is it delivery day?
        if (t_arrival_0[0] if len(t_arrival_0) != 0 else -1) == t:
            current_inventory_0 = current_inventory_0 + replenishment_0[0]
            # remove from the list 
            t_arrival_0.pop(0)
            replenishment_0.pop(0)
        
        
        
        # is it review day?
        if t%sku_0_review_days == 0:
            # reorder if inventory below ROP
            if current_inventory_0 < rop[0]:
                # find order size
                order_0 = max_quantity_SKU_0 - current_inventory_0
                d_0 = 1 # indicate an order took place

                t_arrival_0.append(t + lead_time_mean[0]) # order arrival time period
                replenishment_0.append(order_0) 

        # has there been a stock out?
        if current_inventory_0 < 0:
            s_0 = 1 # indicate there was a stock out
            i_0 = 0 # indicate there's no stock

        # find the cost 
        cost_0 = funcs.cost_function(
                            i=i_0, 
                            inventory=current_inventory_0,
                            per_item_cost=per_item_cost,
                            holding_costs=holding_costs,
                            d=d_0,
                            order_size=order_0,
                            delivery_cost=delivery_cost,
                            s=s_0,
                            stock_out_cost=stock_out_cost)
        
        # save the results 
        # inventory is recorded at the beginning of the day (following a delivery (if any)) 
        # demand_t will affect inventory_t+1
        sim_results["s_" + str(s)]["t_" + str(t)]["SKU_0"] = {
            "SKU": 0,
            "Period": t,
            "Simulation": s,
            "Demand": demand[0][t],
            "Inventory": current_inventory_0,
            "Ordered": order_0,
            "Cost": cost_0
        }

        # find next day's inventory
        inventory[0] = current_inventory_0 - demand[0][t]

        # SKU1

        # SKU2

        # SKU3

        # SKU4


print(sim_results)
