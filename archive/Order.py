class Order:
    def __init__(self,
                 SKUs,
                 quantity,
                 price,
                 delivery_cost,
                 delivery_day) -> None:
        
        
        self.SKUs = SKUs
        self.quantity = quantity
        self.price = price
        self.delivery_cost = delivery_cost
        self.delivery_day = delivery_day

    
    def find_order_price(self) -> float:
        total_price = sum(self.price) + self.delivery_cost

        return total_price

