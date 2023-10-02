
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
        self.risk = risk

