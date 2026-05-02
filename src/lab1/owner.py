from models import Location


class Owner:
    def __init__(self, name):
        self.name = name
        self.animals = []

    def add_animal(self, animal):
        animal.location = Location.OWNER
        self.animals.append(animal)
