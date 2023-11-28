import GA_core as ga_opt

class Individual_Solution(ga_opt.Chromosome):
    """A class representing an inidividual solution (i.e., a collection of policies)

    Attributes:
        skus (list): a list of SKU_Type objects 
    """

    def __init__(self) -> None:
        """A constructor for the Individual_Solution class.

        Args:
            skus (list): a list of SKU_Type objects 
        """
        self.solution = []
        pass
        
        
    def solution_initialize(self,
                            skus) -> None:

        """Initialise the solution
        """
        pass

    def solution_evaluation(self) -> float:

        """Evaluate the fitness of the solution

        Returns:
            float: the fitness of the solution
        """
        pass

    def mutate_chrom(self,
               loc: int) -> None:
        
        """Mutates a policy in the solution

        Args:
            loc (int): location of the mutation
        """

        pass