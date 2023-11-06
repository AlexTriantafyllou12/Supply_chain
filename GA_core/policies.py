
class PolicyInterface():

    def __init__(self, 
                 skus) -> None:
        
        self.skus = skus

  
    def get_params(self) -> None:
        pass
    
  
    def update_params(self, value) -> None:
        pass


class MinMax(PolicyInterface):
    """
    policy with variables - min value (i.e., rop) and max value (i.e., the order-up-to point)
    """

    name = 'minmax'
    
    def __init__(self, skus) -> None:
        
        super().__init__(skus)
        self.min = 0
        self.max = 0

    
    def get_params(self) -> None:
        pass

    def update_params(self, 
                      min=None, 
                      max=None)  -> None:
        pass


class QR(PolicyInterface):
    """
    policy with variables - quantity to order (Q) and reorder point (R)
    """
    name = 'qr'

    def __init__(self, skus) -> None:
        super().__init__(skus)
        self.q_to_order = 0
        self.rop = 0


    def get_params(self) -> None:
        pass

    def update_params(self, 
                      q_to_order=None,
                      rop=None)  -> None:
        pass


class Periodic_Up_To_Point(PolicyInterface):
    """
    periodic policy with variables - time periods and order-up-to value
    """
    name = 'periodic_utp'

    def __init__(self, skus) -> None:
        super().__init__(skus)
        self.time_period = 0
        self.order_up_to = 0


    def get_params(self) -> None:
        pass

    def update_params(self, 
                      time_period=None,
                      order_up_to=None) -> None:
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

