
class SKU:
    """A class representing an SKU type in the inventory 
    
    Attributes:
        name (str): name of the SKU
        quantity (int): quantity of the SKU
    """

    def __init__(self, 
                 name: str,
                 quantity: int,
                 per_item_cost: float) -> None:
        
        """ A constuctor for the SKU class
        """
        
        self.name = name
        self.quantity = quantity
        self.per_item_cost = per_item_cost