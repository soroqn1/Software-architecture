from typing import Dict, Type
from src.lab2.models.animal import Animal
from src.lab2.models.specific_animals import Dog, Owl, Lizard


class AnimalFactory:
    _creators: Dict[str, Type[Animal]] = {
        "собака": Dog,
        "сова": Owl,
        "ящірка": Lizard
    }

    @staticmethod
    def create_animal(animal_type: str, name: str) -> Animal:
        creator = AnimalFactory._creators.get(animal_type.lower())
        if not creator:
            raise ValueError(f"Невідомий тип тварини: {animal_type}")
        return creator(name)

    @staticmethod
    def get_available_types():
        return list(AnimalFactory._creators.keys())
