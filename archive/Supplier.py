from scipy.stats import halfnorm

class Supplier:
    def __init__(self,
                 name,
                 items_delivered,
                 delivery_cost,
                 lead_time,
                 risk) -> None:
        
        self.name = name
        self.items_delivered = items_delivered
        self.delivery_cost = delivery_cost
        self.lead_time = lead_time
        self.risk = risk # standrd deviation of the supplier's lead times

    def find_lead_time(self) -> int:
        lead_time = halfnorm.rvs(loc = self.lead_time, scale = self.risk, size=1)
        return int(lead_time[0])

    def find_sku_price(self,
                    item, 
                    quantity) -> float:
        
        # item is not delivered by the supplier
        if item not in self.items_delivered.keys():
            return 0 
        # find the item's base price
        base_price = quantity * self.items_delivered[item]["price_per_item"]
        discount = 0
        
        # check if the order qualifies for a discount
        for d in self.items_delivered[item]["discount"]:
            if quantity < self.items_delivered[item]["discount"][d]:
                break
                
            discount = d

        # find the SKUs price accounting for the discount (expressed as a percentage)
        sku_price = base_price * (100 - discount) / 100

        return sku_price    
