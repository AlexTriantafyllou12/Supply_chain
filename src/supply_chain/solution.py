import random
import GA_core as ga_opt
import supply_chain as sc

class Individual_Solution(ga_opt.Chromosome):
    """A class representing an inidividual solution (i.e., a collection of policies)

    Attributes:
        skus (list): a list of SKU_Type objects 
    """

    def __init__(self) -> None:
        """A constructor for the Individual_Solution class.

        """
        self.solution = []
        pass
        
        
    def solution_initialize(self,
                            skus: list) -> None:

        """Initialise the solution
        
        Args:
            skus (list): a list of SKU_Type objects 
        
        """

        solution = [] # policies will go here
       
        policy_factory = sc.Policy_Factory()

        for sku in skus:
            # select a random policy type
            policy_type = random.choice(policy_factory.options)
            # create a policy
            policy = policy_factory.create_policy(policy_type, sku)
            # add to the solution
            solution.append(policy)

        return solution




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