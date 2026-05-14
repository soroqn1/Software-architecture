from src.lab2.models.animal import Animal
from src.lab2.core.strategies import RunStrategy, FlyStrategy, CrawlStrategy


class Dog(Animal):
    def __init__(self, name: str):
        super().__init__(name, paws=4, wings=0, movement_strategy=RunStrategy())


class Owl(Animal):
    def __init__(self, name: str):
        super().__init__(name, paws=2, wings=2, movement_strategy=FlyStrategy())


class Lizard(Animal):
    def __init__(self, name: str):
        super().__init__(name, paws=6, wings=0, movement_strategy=CrawlStrategy())
