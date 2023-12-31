import GA_core as ga_opt
import supply_chain as sc

class Genetic_Algorithm:
    """A class representing a genetic algorithm.
    """

    def __init__(self) -> None:
        """A constructor for the Genetic_Algorithm class.
        """
        self.observers = []
        self.population = []
        self.fitness = []
        
    def create_population(self, 
                          size:int, 
                          skus:list) -> None:
        """Generates a population of Individual_Solution objects. 

        Args:
            size (int): the size of the population
            skus (list): a list of SKU_Type objects 

        Returns:
            list: a list of Individual_Solution objects representing a population.
        """

        for i in range(size):
            
            # initialise an individual solution 
            chromosome = sc.Individual_Solution().solution_initialize(skus)
            self.population.append(chromosome)

    
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
                  parents: list,
                  rate: float = 0.9
                  ) -> list:
        """Crossover parent solution to generate two child solutions.

        Args:
            parents (list): parent solutions
            rate (float, optional): probability of the crossover happening. Defaults to 0.9.

        Returns:
            list: a list of Individual_Solution objects representing child solutions.
        """
        pass

    def mutate(self,
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

    def create_observer(self, observer) -> None:
        self.observers.append(observer)

    def notify_observers(self, generation, best_solution) -> None:

        for observer in self.observers:
            observer.update(generation, best_solution)























        
