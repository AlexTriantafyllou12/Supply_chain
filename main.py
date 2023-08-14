import funcs
import random
import pandas as pd

nr_SKUs = 5
avg_lead_time = [random.randint(2, 4) for i in range(5)]

# generate demand 
df_demand = funcs.generate_demand(nr_SKUs=nr_SKUs)

dict_inventory = {} # inventory data for each SKU will go here
list_restrictions = [] # additional data (e.g., safety stock, reorder point) will go here
 
# generate inventory data for each SKU
for i in range(nr_SKUs):
    # find safety stock
    ss = funcs.find_safety_stock(
            demand=df_demand["SKU_"+str(i)],
            max_lead_time=random.randint(5, 7),
            avg_lead_time=avg_lead_time[i]
        )
    
    # find reorder point
    rop = funcs.find_reorder_point(
            demand=df_demand["SKU_"+str(i)],
            avg_lead_time=avg_lead_time[i],
            safety_stock=ss
    )

    # generate inventory data
    inv = funcs.generate_inventory(
            demand=df_demand["SKU_"+str(i)],
            reorder_point=rop,
            max_capacity=rop*5
    )

    # add the additional data to the list 
    list_restrictions.append(
        {
            "SKU": "SKU_"+str(i),
            "SS": ss,
            "ROP": rop
        }
    )
    # add the inventory data to the dictionary
    dict_inventory["SKU_inventory_"+str(i)] = inv
    
    print("Safety stock for SKU_{0} is {1} units".format(i,ss))
    print("Reorder point for SKU_{0} is {1} units".format(i,rop))

# convert the dictionary of inventory data into a dataframe
df_inventory = pd.DataFrame(dict_inventory)
# combine the demand and inventory datasets
df_full_dataset = pd.concat([df_demand, df_inventory], axis=1)
df_full_dataset.to_csv('data/full_dataset.csv', index=False)

# convert the list of additional data to a dataframe
df_restrictions = pd.DataFrame(list_restrictions)
df_restrictions.to_csv('data/restrictions.csv', index=False)

print(df_restrictions)