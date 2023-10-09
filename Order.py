class Order:
    def __init__(self,
                 SKUs,
                 quantity,
                 price,
                 delivery_day) -> None:
        
        
        self.SKUs = SKUs
        self.quantity = quantity
        self.price = price
        self.delivery_day = delivery_day

    
    def find_order_price(self) -> float:
        total_price = sum(self.price)

        return total_price

