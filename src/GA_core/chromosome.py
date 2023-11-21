from abc import ABC, abstractmethod
import GA_core as ga_opt


class Chromosome(ABC):
        
    @abstractmethod 
    def solution_initialize(self) -> list[ga_opt.Gene]:

        """Initialise the solution
        """
        pass
    
    @abstractmethod
    def solution_evaluation(self, 
                            fitness_func) -> float:

        """Evaluate the fitness of the solution

        Returns:
            float: the fitness of the solution
        """
        pass

    @abstractmethod
    def mutate_chrom(self,
                    loc: int) -> None:
        
        """Mutates a policy in the solution

        Args:
            loc (int): location of the mutation
        """

        pass