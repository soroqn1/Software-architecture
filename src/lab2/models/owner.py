from typing import List
from src.lab2.models.animal import Animal, Location
from src.lab2.core.events import AnimalEventArgs, DeathEventArgs, HungerEventArgs


class Owner:
    def __init__(self, name: str):
        self.name = name
        self.animals: List[Animal] = []

    def adopt_animal(self, animal: Animal):
        animal.location = Location.OWNER
        self.animals.append(animal)

        animal.on_died.subscribe(self._on_animal_died)
        animal.on_hungry.subscribe(self._on_animal_hungry)
        #animal.on_action.subscribe(self._on_animal_action)

    def _on_animal_died(self, sender: Animal, args: DeathEventArgs):
        pass

    def _on_animal_hungry(self, sender: Animal, args: HungerEventArgs):
        pass

    def release_animal(self, animal: Animal):
        if animal in self.animals:
            animal.location = Location.WILD
            self.animals.remove(animal)
            animal.on_died.unsubscribe(self._on_animal_died)
            animal.on_hungry.unsubscribe(self._on_animal_hungry)
