import GA_core as ga_opt
import supply_chain as sc
import random

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
            chromosome = sc.Individual_Solution()
            chromosome.solution_initialize(skus)
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
                  parentsA: list,
                  parentsB: list,
                  rate: float = 0.9
                  ) -> list:
        """Crossover parent solution to generate two child solutions.

        Args:
            parents (list): parent solutions
            rate (float, optional): probability of the crossover happening. Defaults to 0.9.

        Returns:
            list: a list of Individual_Solution objects representing child solutions.
        """

        children = [] # child solution go here

        for i, p in enumerate(parentsA):
            # define the parents
            parentA = p
            parentB = parentsB[i]

            # randomly determine if crossover takes place
            if random.random() < rate:

                # instantiate the factory
                factory = ga_opt.Crossover_Factory()
                crossover_type = random.choice(factory.options)
                child1, child2 = factory.create_crossover(crossover_type, parentA, parentB)

                children.append(child1)
                children.append(child2)
            
            else:
                children.append(parentA)
                children.append(parentB)
        
        return children


    def mutate(self,
               rate: float = 0.3) -> None:
        """Mutates a random policy in the solution provided.

        Args:
            rate (float, optional): probability of the mutations happening. Defaults to 0.9.
        """
        
        # randomly determine if the mutation takes place
        for i, s in enumerate(self.population):
             
            if random.random() < rate:
             
                solution_length = len(s.solution)
                # determine the location of the mutation
                mutation_loc = random.randint(0, solution_length-1)
                s.mutate_chrom(loc = mutation_loc)


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

    def notify_observers(self, generation, best_score, best_solution) -> None:

        for observer in self.observers:
            observer.update(generation, best_score, best_solution)























        
