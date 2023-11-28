import GA_core as ga_opt

class ProgressObserver:
    """A class representing a progress observer.
    """
    def update(self, 
               generation: int, 
               best_score: float,
               best_solution: ga_opt.Chromosome):
        """Updates observer about the progress of the GA

        Args:
            generation (int): the number of the generation
            best_score (float): the fitness of the solution
            best_solution (Individual_Solution): Individual_Solution object with the best fitness
        """
        print(f"Generation {generation}: Best solution - {best_score}")