import funcs
import random
import numpy as np

# define the restrictions
lead_time_mean  = [3, 5]
lead_time_sd    = [2, 1]

nr_SKUs         = 3
nr_sims         = 10

demand_mean     = [random.randint(300, 600) for i in range(nr_SKUs)]
demand_sd       = [random.randint(50, 100) for i in range(nr_SKUs)]

holding_costs   = 0.05 # percent of the total cost of the item stored
delivery_cost   = 100 # constant per delivery
stock_out_cost  = 100000
per_item_cost   = 100
time_periods    = 10
scrap_value     = 300

sim_results     = {} # simulation results will go here

# generate demand per SKU
demand = funcs.generate_demand(
    nr_SKUs=nr_SKUs,
    time_periods=time_periods,
    demand_mean=demand_mean,
    demand_sd=demand_sd
)

# assume starting inventory is 5 times the demand on day 1 for each SKU
starting_inventory = np.asarray([demand[i][0] * 5 for i in range(nr_SKUs)])

#print("Demand: ", demand)

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

#print("ROP: ", rop)

# sampling population for the periodic review policy
periodic_review_periods = np.arange(1,90,1)

# sampling population for the 'order up to a point' policy
max_quantity = np.arange(1000, 20000, 500)

# sampling population for the 'constant quantity' policy
contant_quantity = np.arange(500, 20000, 500)

print("Periodic Review: ", periodic_review_periods[2])
print("Max Quanity: ", max_quantity[3])
print("Constant Quantity: ", contant_quantity[9])

#cost function 
# cost_func = carry_over_costs + delivery_cost + stock_out_cost


# sampling from
# different interval lengths 
# reorder point, this would be a binomal choice 
# no overlap between the suppliers, say one supplier supplies 2 SKUs the other 

# each iteration is a 

#for sample_inventory_policies:
 # SKU0 = periodic review, order up to a point
 # SKU1 = reorder once inventory levels reach reorder point (rop), constant quantity
 # SKU2 = reorder once inventory levels reach rop, order up to a point
 # SKU3 = reorder once inventory levels reach rop, constant quantity
 # SKU4 = periodic review, periodic review
inventory = starting_inventory

for s in range(nr_sims):

    review_period_SKU_0     = random.choice(periodic_review_periods)
    constant_quantity_SKU_1 = random.choice(contant_quantity)
    max_quantity_SKU_2      = random.choice(max_quantity)
    contant_quantity_SKU_3  = random.choice(contant_quantity)
    review_period_SKU_4     = random.choice(periodic_review_periods)

    for t in time_periods:
        
        # SKU0 & SKU4
        for s0 in range(nr_sims):
            max_quantity_SKU_0      = random.choice(max_quantity)
            contant_quantity_SKU_4  = random.choice(contant_quantity)


        # SKU1


        # SKU2


        # SKU3
    

    # d & z are either 0 or 1
    # cost_func_t = inventory_t-1 * per_item_cost * holding_costs + d * delivery_cost + s * stock_out_cost

    
#     sim_results.append(
#         {
#             "SKU": "SKU_" + str(0)
#             "Period": t,
#             "Simulation": "sim_" + str(x),
#             "Inventory":
#             "Ordered":
#             "Cost"
#         }
#     )
