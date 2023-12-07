from abc import ABC, abstractmethod
import GA_core as ga_opt
import utilities as u
import random

class Crossover(ABC):
    """A class representing the crossover interface.

    Args:
        ABC (class): Abstract class
    """

    @abstractmethod
    def crossover(self, 
                  parentA: ga_opt.Chromosome, 
                  parentB: ga_opt.Chromosome) -> ga_opt.Chromosome:
        """Placeholder for the corssover functions.

        Args:
            parentsA (list): list of Individual_Solution objects representing parent solutions

        Returns:
            list: list of Individual_Solution objects representing child solutions.
        """
        pass


class Crossover_single(Crossover):
    """Single crossover class.

    """

    def crossover(self, 
                  parentA: ga_opt.Chromosome,
                  parentB: ga_opt.Chromosome) -> ga_opt.Chromosome:
        
        """Crosses over two parent solutions at a single random point.

        Args:
            parentA (Chromosome): a parent solution.
            parentB (Chromosome): a parent solution
        
        Returns:
            Chromosome: return two child solutions
        """
        
        solution_length = len(parentA.solution)

        # select a random crossover point
        cp = random.randint(1, solution_length - 1)

        crossover1 = parentA.solution[0:cp] + parentB.solution[cp:]
        crossover2 = parentB.solution[0:cp] + parentA.solution[cp:]
        
        # update parent objects to create child objects
        parentA.solution_update(crossover1)
        parentB.solution_update(crossover2)
        
        # return two new child solutions
        return parentA, parentB


class Crossover_double(Crossover):
    """Double crossover class.

    """


    def crossover(self, 
                  parentA: ga_opt.Chromosome,
                  parentB: ga_opt.Chromosome) -> ga_opt.Chromosome:
        
        """Crosses over two parent solutions at two random points.

        Args:
            parentA (Chromosome): a parent solution.
            parentB (Chromosome): a parent solution
        
        Returns:
            Chromosome: return two child solutions
        """
        
        solution_length = len(parentA.solution)

        # select a random crossover point
        cp1 = random.randint(1, solution_length - 1)
        cp2 = random.randint(cp1, solution_length - 1)

        # double crossover
        crossover1 = parentA.solution[0:cp1] + parentB.solution[cp1:cp2] + parentA.solution[cp2:]
        crossover2 = parentB.solution[0:cp1] + parentA.solution[cp1:cp2] + parentB.solution[cp2:]

        # update parent objects to create child objects
        parentA.solution_update(crossover1)
        parentB.solution_update(crossover2)

        return parentA, parentB


class Crossover_Factory():
    """A class implementing the factory design pattern.

    Raises:
        ValueError: raises an error if an invalid crossover type is provided.

    Returns:
        list: list of Individual_Solution objects representing child solutions.
    """
    options = ["1", "2"]

    @staticmethod
    def create_crossover(type:str, 
                  parentA: ga_opt.Chromosome,
                  parentB: ga_opt.Chromosome) -> ga_opt.Chromosome:
        """Crosses over parent solutions given the specified type

        Args:
            type (str): type of the crossover
            parents (list): list of Individual_Solution objects representing parent solutions

        Raises:
            ValueError: raises an error if an invalid crossover type is provided.

        Returns:
            list: list of Chromosome objects representing child solutions.
        """

        if type == '1':
            return Crossover_single().crossover(parentA, parentB)
        elif type == '2':
            return Crossover_double().crossover(parentA, parentB)
        
        else: raise ValueError("Crossover type not valid.")