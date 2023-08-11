# Cost Optmisation Model 

## The Problem: 
- Cost of raw materials (e.g., chemicals) fluctuates over time, based on quantity bought and across suppliers.
- Total has certain demand to meet which requires X amount of chemicals Y and Z to produce.
- Totals has the capacity to keep an inventory of raw materials (limited).

## Objective:
Minimize costs. 

## Questions:
The overarching question is: How should Total schedule the ordering of raw materials to satisfy the demand and comply with the inventory restrictions while minimizing cost?
This can be further broken down into questions:

**Descriptive:**
- How much demand can Total fulfill with the current inventory?
- What's the average price of raw materials over the past X months? How does it compare with the current price?
- What is the minimum reorder point for each material? How do the inventory levels compare to the reorder point (past it, approaching, etc)?
- What's the cost of raw materials to produce one unit of oil?...

**Predictive:**
- Which supplier should Total order from?
- How much raw materials should Total order?
- When should Total place the order?

## Restrictions:
- Lead times for each supplier
- Delivery costs
- Holding costs
- Inventory capacity
- Safety stock
- Supplier A offers a 3% discount with order size X
- Supplier B offers a 5% discount with order size Y

## Output:
- Optimizer
- Dashboard
