class PolicyInterface:

    def find_quantity_to_order(self) -> None:
        pass

    def order(self) -> None:
        pass


class MinMax(PolicyInterface):
    """
    continous policy with variables - min value (i.e., rop) and max value (i.e., the order-up-to point)
    """
    
    def find_quantity_to_order(self) -> None:
        pass

    def order(self) -> None:
        pass


class QR(PolicyInterface):
    """
    continous policy with variables - quantity to order (Q) and reorder point (R)
    """

    def find_quantity_to_order(self) -> None:
        pass

    def order(self) -> None:
        pass


class Periodic_Up_To_Point(PolicyInterface):
    """
    periodic policy with variables - time periods and order-up-to value
    """

    def find_quantity_to_order(self) -> None:
        pass

    def order(self) -> None:
        pass


class Policy_Factory:

    @staticmethod
    def create_policy(type):
        if type == 'minmax':
            return MinMax()
        elif type == 'qr':
            return QR()
        elif type == 'periodic_utp':
            return Periodic_Up_To_Point()
        
        else: raise ValueError("nope...")