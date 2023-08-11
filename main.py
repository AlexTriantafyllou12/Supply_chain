import funcs
import random

nr_SKUs = 5

# generate demand 
demand = funcs.generate_demand(nr_SKUs=nr_SKUs)

# find the safety stock for each SKU
for i in range(nr_SKUs):
    ss = funcs.find_safety_stock(
            demand=demand["SKU_"+str(i)],
            max_lead_time=random.randint(3, 10),
            avg_lead_time=random.randint(2, 5)
        )
    
    print("Safety stock for SKU_{0} is {1} units".format(i,ss))