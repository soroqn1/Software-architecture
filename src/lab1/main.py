from datetime import datetime
from enum import Enum


class Location(Enum):
    OWNER = "Хазяїн"
    PET_SHOP = "Зоомагазин"
    WILD = "Воля"


class Animal:
    def __init__(self, name):
        self.name = name

        self.eyes = 2
        self.paws = 4
        self.wings = 0

        self.location = Location.WILD
        self.last_meal_time = datetime.now()
        self.meals_today = 0
        self.is_alive = True

        self.on_died = []
        self.on_hungry = []

    def eat(self):
        pass

    def move(self):
        pass

    def check_status(self):
        hours_passed = (datetime.now() - self.last_meal_time).total_seconds() / 3600

        if not self.is_alive:
            return

        if hours_passed >= 24:
            self.is_alive = False
            for callback in self.on_died:
                callback(self)
        elif hours_passed >= 8:
            for callback in self.on_hungry:
                callback(self)


class Dog(Animal):
    def __init__(self, name):
        super().__init__(name)


class Owl(Animal):
    def __init__(self, name):
        super().__init__(name)

        self.wings = 2


class Lizard(Animal):
    def __init__(self, name):
        super().__init__(name)

        self.paws = 6
