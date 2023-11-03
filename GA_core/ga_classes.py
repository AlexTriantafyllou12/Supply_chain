
class ProgressObserver:
    def update(self, generation, best_score):
        print(f"Generation {generation}: Best solution - {best_score}")


class Genetic_Algorithm:

    def __init__(self) -> None:
        self.observers = []
        
        def create_population(self) -> None:
            pass
        
        def evaluate_population(self) -> None:
            pass

        def select_parents(self) -> None:
            pass

        def crossover(self) -> None:
            pass
    
        def mutate(self) -> None:
            pass

        def evolve(self) -> None:
            pass

        def run_genetic(self, generations) -> None:

            self.create_population()

            for generation in range(generation):
                population_new = []

            pass

        def create_observer(self, observer):
            self.observers.append(observer)

        def notify_observers(self, generation, best_solution):

            for observer in self.observers:
                observer.update(generation, best_solution)



class Individual_Solution:

    def __init__(self) -> None:
        
        
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


class CrossoverInterface:

    def crossover(self, parents) -> None:
        pass



class Crossover_var1(CrossoverInterface):

    def crossover(self, parents) -> None:
        pass


class Crossover_var2(CrossoverInterface):

    def crossover(self, parents) -> None:
        pass


class Crossover_Factory:

    @staticmethod
    def create_crossover(type):
        if type == '1':
            return Crossover_var1()
        elif type == '2':
            return Crossover_var2()
        
        else: raise ValueError("nope...")



















        
