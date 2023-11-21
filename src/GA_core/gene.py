from abc import ABC, abstractmethod


class Gene(ABC):

    @abstractmethod
    def mutate_gene(self):
        pass