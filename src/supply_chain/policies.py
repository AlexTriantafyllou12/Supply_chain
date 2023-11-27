from abc import ABCMeta, abstractmethod
import GA_core as ga_opt


class Policy(metaclass=ABCMeta):

    @abstractmethod
    def get_params(self) -> dict:
        """Returns class attributes as a dictionary.

        Returns:
            dict: returns a dictionary with the attributes of the class
        """
        pass



class MinMax(PolicyInterface, ga_opt.Gene):
    """A class used to represent minmax inventory policy.

    Args:
        DemandInterface (class): Abstract parent class
    
    Attributes:
        skus (dict): a dictionary of SKUType objects
        min (int, optional): minimum reordering point. Set to 0 by default.
        max (int, optional): maximum order-up-to point. Set to 0 by default.
    """


    name = 'minmax'
    
    def __init__(self, 
                 skus: dict,
                 min: int = 0,
                 max: int = 0) -> None:
        """Constructor for MinMax class.

        Args:
            skus (dict): a dictionary of SKUType objects
            min (int, optional): minimum reordering point. Set to 0 by default.
            max (int, optional): maximum order-up-to point. Set to 0 by default.
        """
        self.skus = skus
        self.min = min
        self.max = max

    
    def get_params(self) -> dict:
        """Returns class attributes as a dictionary.

        Returns:
            dict: returns a dictionary with the attributes of the class
        """
        pass

    def mutate_gene(self, 
                      min:int = None, 
                      max: int = None)  -> None:
        """Update min and/ or max class attributes 

        Args:
            min (int, optional): the new min value to be updated. Defaults to None.
            max (int, optional): the new max value to be updated. Defaults to None.
        """
        pass


class QR(PolicyInterface, ga_opt.Gene):
    """A class used to represent (Q, R) inventory policy.

    Args:
        DemandInterface (class): Abstract parent class
    
    Attributes:
        skus (dict): a dictionary of SKUType objects
        q_to_order (int, optional): the quantity to order. Defaults to 0.
        rop (int, optional): the reordering point. Defaults to 0.        
    """

    name = 'qr'

    def __init__(self, 
                 skus: dict,
                 q_to_order: int = 0,
                 rop: int = 0) -> None:
        """Constructor for QR class.

        Args:
            skus (dict): a dictionary of SKUType objects.
            q_to_order (int, optional): the quantity to order. Defaults to 0.
            rop (int, optional): the reordering point. Defaults to 0.
        """
        self.skus = skus
        self.q_to_order = q_to_order
        self.rop = rop


    def get_params(self) -> dict:
        """Returns class attributes as a dictionary.

        Returns:
            dict: returns a dictionary with the attributes of the class
        """        
        pass

    def mutate_gene(self, 
                      q_to_order:int = None,
                      rop:int = None)  -> None:
        """Update q_to_order and/or rop class attributes.

        Args:
            q_to_order (int, optional): the new q_to_order value to be updated. Defaults to None.
            rop (int, optional): the new rop value to be updated. Defaults to None.
        """
        pass


class Periodic_Up_To_Point(PolicyInterface, ga_opt.Gene):
    """A class used to represent a periodic inventory policy.

    Args:
        DemandInterface (class): Abstract parent class
    
    Attributes:
        skus (dict): a dictionary of SKUType objects.
        time_period (int, optional): Frequency of inventory reviews. Defaults to 0.
        order_up_to (int, optional): Order-up-to quantity. Defaults to 0.       
    """

    
    name = 'periodic_utp'

    def __init__(self, 
                 skus: dict,
                 time_period: int = 0,
                 order_up_to: int = 0) -> None:
        """Constructor for Periodic_Up_To_Point class.

        Args:
            skus (dict): a dictionary of SKUType objects.
            time_period (int, optional): Frequency of inventory reviews. Defaults to 0.
            order_up_to (int, optional): Order-up-to quantity. Defaults to 0.
        """
        self.skus = skus
        self.time_period = time_period
        self.order_up_to = order_up_to


    def get_params(self) -> dict:
        """Returns class attributes as a dictionary.

        Returns:
            dict: returns a dictionary with the attributes of the class
        """        
        pass

    def muate_gene(self, 
                      time_period:int = None,
                      order_up_to:int = None) -> None:
        """Update time_period and/or order_up_to class attributes.

        Args:
            time_period (int, optional): the new time_period value to be updated. Defaults to None.
            order_up_to (int, optional): the new order_up_to value to be updated. Defaults to None.
        """
        pass


class Policy_Factory:

    @staticmethod
    def create_policy(type, skus):
        if type == 'minmax':
            return MinMax(skus)
        elif type == 'qr':
            return QR(skus)
        elif type == 'periodic_utp':
            return Periodic_Up_To_Point(skus)
        
        else: raise ValueError("Policy type not valid")


