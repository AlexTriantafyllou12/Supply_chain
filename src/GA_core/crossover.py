from abc import ABC, abstractmethod

class CrossoverInterface(ABC):
    """A class representing the crossover interface.

    Args:
        ABC (class): Abstract class
    """

    @abstractmethod
    def crossover(self, 
                  parents: list) -> list:
        """Placeholder for the corssover functions.

        Args:
            parents (list): list of Individual_Solution objects representing parent solutions

        Returns:
            list: list of Individual_Solution objects representing child solutions.
        """
        pass


class Crossover_var1(CrossoverInterface):

    def crossover(self, 
                  parents:list) -> None:
        pass


class Crossover_var2(CrossoverInterface):

    def crossover(self, 
                  parents:list) -> None:
        pass


class Crossover_Factory():
    """A class implementing the factory design pattern.

    Raises:
        ValueError: raises an error if an invalid crossover type is provided.

    Returns:
        list: list of Individual_Solution objects representing child solutions.
    """

    @staticmethod
    def create_crossover(type:str, 
                         parents: list):
        """Crosses over parent solutions given the specified type

        Args:
            type (str): type of the crossover
            parents (list): list of Individual_Solution objects representing parent solutions

        Raises:
            ValueError: raises an error if an invalid crossover type is provided.

        Returns:
            list: list of Individual_Solution objects representing child solutions.
        """

        if type == '1':
            return Crossover_var1()
        elif type == '2':
            return Crossover_var2()
        
        else: raise ValueError("nope...")