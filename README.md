# Invenotry Simulation 

## Project Overview

### Background & Challenge 

In Oil & Gas multiple critical processes are dependent on chemicals. Among others, these include:
  
-	**E&P value cycle:**  If a geological system gives the confidence that there is working petroleum, exploration, appraisal, and production wells will be drilled; this process requires a lot of chemicals to be available (one-off or continuous inflow)

-	**Late field life:** when a field starts producing only water, this water will need to be purified

Chemicals need to be available at the right time and place, as production must continue at all costs. It is expected that one day’s Production is worth much more than the overall spending on chemicals in one year. Operators will “over” pay for chemicals due to the high opportunity cost. 


### Objective

How should the ordering and storage of raw materials/chemicals be scheduled to ensure production uptime and compliance with the inventory restrictions while minimizing cost?  

### Solution

The solution is a **simulation-based approach** to inventory and procurement planning which allows for the exploration of different planning scenarios to better understand the impact of each variable (number of suppliers, lead times, capacity constraints, etc) on inventory management.


The **simulator** iterates through random inventory policy configurations to find the optimal combination of policies for all items for the specified time period. In each simulation, the following parameters are explored:
-	Policy type (Periodic or Continuous) 
-	Review period (Days)
-	Quantity to order 






## Code Base

### UML Diagram


![](imgs/uml.png)

###  Scenario 
The following section describes the simulated scenario and highlights the use of functions at each step.

1.	Define the SKUs, Suppliers and Warehouses to be used in the simulation.
    - `SKU.generate_demand()`
    - `SKU.set_demand()`
    - `SKU.find_rop()`
    - `SKU.set_rop()`
2.	The simulation iterates through a number of runs (nr_runs).
    -	`Simulation.run_sim()`
3.	At the beginning of each simulation, each SKU is assigned a random policy, review period and maximum quantity (depending on the max quantity of the warehouse).
    -	`Warehouse.allocate_space()`
    -	`SKU.set_max_quantity()`
    -	`SKU.set_policy()`
    -	`SKU.set_review_period()`
    -	`SKU.generate_starting_invenotry()`
    -	`SKU.set_actual_invenotry()`
    -	`SKU.set_estimated_invenotry()`
4.	Each simulation will iterate through a number of days/ periods.
5.	On each day, iterate through the items to check if the inventory needs to be evaluated. 
    -	If the inventory needs to be evaluated:
        -	Check the **estimated** inventory against the ROP, if actual_invenotry < ROP:
            -	Find the quantity to order.
                -	`SKU.find_quantity_to_order()`
            -	Add the item to a list of items to order.
            -	Update the estimated inventory (current + ordered - consumed). 
                -	`SKU.set_estimated_invenotry()`
            -	Check the **actual** inventory for stockouts.
6.	At the end of the day:
    -	Assign items to suppliers (i.e., place the orders).
        -	`Supplier.find_sku_price()`
        -	`Supplier.find_lead_time()`
    -	Find the total cost per order.
        -	`Order.find_order_price()`
    -	Check for deliveries:
        -	`SKU.set_actual_inventory()`
        -	`Warehouse.set_current_capacity()`
    -	Check warehouse capacity vs. max capacity.
        -	 If current capacity > max capacity, scrap the overstocked SKUs.
             -	`Warehouse.scrap()`
             -	`SKU.set_actual_inventory()`
             -	`SKU.set_estimated_invenotry()`
    -	Find the daily total cost: 
        -	`Utility.cost_function()`

### Assumptions 

The following assumptions have been made in creating the simulation:
-	Some chemicals are used more frequently than others (demand variability).
-	Each chemical has a set reorder point (ROP) and safety stock (SS) modelled based on the assumed uncertainty of the demand and supplier lead times.
-	Suppliers have different lead times – these are not always constant and there is uncertainty involved.
-	Suppliers have a constant delivery fee regardless of the size of the order.
-	Suppliers offer different quotas based on the number of units ordered – the higher the number the lesser the per unit cost.
-	Chemicals are stored in warehouses, up until they are used.
-	We consider a ‘holding’ cost for each period that an invenotry is stored that consists of a fixed warehouse holding cost and a fee per each item stored.
-	The holding cost includes space, work capital, etc. 

