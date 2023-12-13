from abc import ABCMeta, abstractmethod
import GA_core as ga_opt
import supply_chain as sc


class Policy(metaclass=ABCMeta):

    @abstractmethod
    def get_params(self) -> dict:
        """Returns class attributes as a dictionary.

        Returns:
            dict: returns a dictionary with the attributes of the class
        """
        pass

    @abstractmethod
    def order_quantity(self) -> int:
        """Determine the quantity to order.

        Returns:
            int: order quantity
        """

        pass

    @abstractmethod
    def check_if_order_needed(self) -> bool:
        """Check if an order needs to be placed given the current invenotry level

        Returns:
            bool: True/ False
        """
        pass



class MinMax(Policy, ga_opt.Gene):
    """A class used to represent minmax inventory policy.

    Args:
        DemandInterface (class): Abstract parent class
    
    Attributes:
        sku (SKU): SKU object
        min (int, optional): minimum reordering point. Set to 0 by default.
        max (int, optional): maximum order-up-to point. Set to 0 by default.
    """


    name = 'minmax'
    
    def __init__(self, 
                 sku: sc.SKU,
                 min: int = 50,
                 max: int = 300) -> None:
        """Constructor for MinMax class.

        Args:
            sku (SKU): SKU object
            min (int, optional): minimum reordering point. Set to 0 by default.
            max (int, optional): maximum order-up-to point. Set to 0 by default.
        """
        self.sku = sku
        self.min = min
        self.max = max

    
    def get_params(self) -> dict:
        """Returns class attributes as a dictionary.

        Returns:
            dict: returns a dictionary with the attributes of the class
        """
        pass

    def mutate_gene(self)  -> None:
        """Update min and/ or max class attributes 

        """
        pass

    def order_quantity(self,
                          qoh: int,
                          on_order: int) -> int:
        """Determine the quantity to order.

        Args:
            qoh (int): quantity on hand (i.e., in inventory)
            on_order (int): quantity on order

        Returns:
            int: order quantity
        """

        order_quantity = self.max - qoh - on_order
        
        return order_quantity
        
    def check_if_order_needed(self,
                              qoh: int,
                              on_order: int,
                              period: int) -> bool:
        """Check if an order needs to be placed given the current invenotry level

        Args:
            qoh (int): quantity on hand (i.e., in inventory)
            on_order (int): quantity on order
            period (int): time period at the time of checking the inventory

        Returns:
            bool: True/ False
        """
        
        if (qoh + on_order) < self.min:
            return True
        
        return False



class QR(Policy, ga_opt.Gene):
    """A class used to represent (Q, R) inventory policy.

    Args:
        DemandInterface (class): Abstract parent class
    
    Attributes:
        sku (SKU): SKU object
        q_to_order (int, optional): the quantity to order. Defaults to 0.
        rop (int, optional): the reordering point. Defaults to 0.        
    """

    name = 'qr'

    def __init__(self, 
                 sku: sc.SKU,
                 q_to_order: int = 300,
                 rop: int = 90) -> None:
        """Constructor for QR class.

        Args:
            sku (SKU): SKU object
            q_to_order (int, optional): the quantity to order. Defaults to 0.
            rop (int, optional): the reordering point. Defaults to 0.
        """
        self.sku = sku
        self.q_to_order = q_to_order
        self.rop = rop


    def get_params(self) -> dict:
        """Returns class attributes as a dictionary.

        Returns:
            dict: returns a dictionary with the attributes of the class
        """        
        pass

    def mutate_gene(self)  -> None:
        """Update q_to_order and/or rop class attributes.
        """
        pass

    def order_quantity(self, 
                        qoh: int,
                        on_order: int) -> int:
        """Determine the quantity to order.

        Args:
            qoh (int): quantity on hand (i.e., in inventory)
            on_order (int): quantity on order

        Returns:
            int: order quantity
        """
        
        return self.q_to_order


    def check_if_order_needed(self,
                              qoh: int,
                              on_order: int,
                              period: int) -> bool:
        """Check if an order needs to be placed given the current time period

        Args:
            qoh (int): quantity on hand (i.e., in inventory)
            on_order (int): quantity on order
            period (int): time period at the time of checking the inventory

        Returns:
            bool: True/ False
        """
        
        # check if the current invenotry is bellow rop
        if qoh < self.rop:
            return True
        
        return False


class Periodic_Up_To_Point(Policy, ga_opt.Gene):
    """A class used to represent a periodic inventory policy.

    Args:
        DemandInterface (class): Abstract parent class
    
    Attributes:
        sku (SKU): SKU object
        time_period (int, optional): Frequency of inventory reviews. Defaults to 0.
        order_up_to (int, optional): Order-up-to quantity. Defaults to 0.       
    """

    
    name = 'periodic_utp'

    def __init__(self, 
                 sku: sc.SKU,
                 time_period: int = 4,
                 order_up_to: int = 400) -> None:
        """Constructor for Periodic_Up_To_Point class.

        Args:
            sku (SKU): SKU object
            time_period (int, optional): Frequency of inventory reviews. Defaults to 0.
            order_up_to (int, optional): Order-up-to quantity. Defaults to 0.
        """
        self.sku = sku
        self.time_period = time_period
        self.order_up_to = order_up_to


    def get_params(self) -> dict:
        """Returns class attributes as a dictionary.

        Returns:
            dict: returns a dictionary with the attributes of the class
        """        
        pass

    def mutate_gene(self) -> None:
        """Update time_period and/or order_up_to class attributes.

        """
        print('Mutated..')
    
    def order_quantity(self, 
                        qoh: int,
                        on_order: int) -> int:
        """Determine the quantity to order.

        Args:
            qoh (int): quantity on hand (i.e., in inventory)
            on_order (int): quantity on order

        Returns:
            int: order quantity
        """

        # check that qoh doesn't exceed order up to point
        if qoh < self.order_up_to:
            order_quantity = self.order_up_to - qoh
            
        else:
            order_quantity = 0
        
        return order_quantity


    def check_if_order_needed(self,
                              qoh: int,
                              on_order: int,
                              period: int) -> bool:
        """Check if an order needs to be placed given the current time period

        Args:
            qoh (int): quantity on hand (i.e., in inventory)
            on_order (int): quantity on order
            period (int): time period at the time of checking the inventory

        Returns:
            bool: True/ False
        """
        
        # check if the policy order period mathces the current time period
        if period % self.time_period == 0:
            return True
        
        return False
    


class Policy_Factory:
    options = ['minmax', 'qr', 'periodic_utp'] 

    @staticmethod
    def create_policy(type: str, 
                      sku: sc.SKU):
        
        if type == 'minmax':
            return MinMax(sku)
        elif type == 'qr':
            return QR(sku)
        elif type == 'periodic_utp':
            return Periodic_Up_To_Point(sku)
        
        else: raise ValueError("Policy type not valid")


