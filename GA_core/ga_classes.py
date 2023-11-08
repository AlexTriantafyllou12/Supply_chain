from abc import ABC, abstractmethod

class ProgressObserver:
    def update(self, generation, best_score):
        print(f"Generation {generation}: Best solution - {best_score}")


class Individual_Solution:

    def __init__(self) -> None:
        pass
        
        
    def solution_initialize(self) -> None:

        """
        create a solution
        """
        pass

    def solution_evaluation(self) -> None:

        """
        evaluate the fitness of solution based on a given function
        """
        pass

    def mutate(self) -> None:

        """
        apply small random changes in a solution
        """
        pass


class CrossoverInterface(ABC):

    @abstractmethod
    def crossover(self, parents) -> None:
        pass



class Crossover_var1(CrossoverInterface):

    def crossover(self, parents) -> None:
        pass


class Crossover_var2(CrossoverInterface):

    def crossover(self, parents) -> None:
        pass


class Crossover_Factory():

    @staticmethod
    def create_crossover(type):
        if type == '1':
            return Crossover_var1()
        elif type == '2':
            return Crossover_var2()
        
        else: raise ValueError("nope...")

class Genetic_Algorithm:
    """A class representing a genetic algorithm.
    """

    def __init__(self) -> None:
        self.observers = []
        self.population = []
        self.fitness = []
        
    def create_population(self, 
                          size:int, 
                          skus:list) -> list:
        """Generates a population of Individual_Solution objects. 

        Args:
            size (int): the size of the population
            skus (list): a list of SKU_Type objects 

        Returns:
            list: a list of Individual_Solution objects representing a population.
        """
        pass
    
    def evaluate_population(self) -> list:
        """Evaluates the fitness of each solution in the population.

        Returns:
            list: a list of fitness scores
        """
        pass

    def select_parents(self, 
                       pool_size:int  = 3) -> list:
        """Selects parent solutions according to tournament selection.

        Args:
            pool_size (int, optional): the number of solution sampled from the population, i.e., the tournament size

        Returns:
            list: a list of selected parent solutions.
        """
        pass

    def crossover(self,
                  parent1: Individual_Solution,
                  parent2: Individual_Solution,
                  rate: float = 0.9
                  ) -> list:
        """Crossover parent solution to generate two child solutions.

        Args:
            parent1 (Individual_Solution): the first parent solution
            parent2 (Individual_Solution): the second parent solution
            rate (float, optional): probability of the crossover happening. Defaults to 0.9.

        Returns:
            list: a list of Individual_Solution objects representing child solutions.
        """
        pass

    def mutate(self,
               individual: Individual_Solution,
               rate: float = 0.9) -> None:
        """Mutates a random policy in the solution provided.

        Args:
            individual (Individual_Solution): the solution to be mutated.
            rate (float, optional): probability of the mutations happening. Defaults to 0.9.
        """
        pass

    def evolve(self,
               next_gen: list) -> None:
        """Updates the population attribute.

        Args:
            next_gen (list): a list of Individual_Solution objects.
        """
        pass

    def run_genetic(self,
                    population: list,
                    crossover_rate:float = 0.9,
                    mutation_rate: float = 0.9, 
                    generations:int = 100) -> None:
        """Runs the genetic algorithm. 

        Args:
            population (list): a list of Individual_Solution objects representing a population. 
            crossover_rate (float, optional): probability of the crossover happening. Defaults to 0.9.
            mutation_rate (float, optional): probability of the mutations happening. Defaults to 0.9.
            generations (int, optional): the number of generations for the algorithm to run for. Defaults to 100.
        """

        print('running..')

    def create_observer(self, observer):
        self.observers.append(observer)

    def notify_observers(self, generation, best_solution):

        for observer in self.observers:
            observer.update(generation, best_solution)























        
