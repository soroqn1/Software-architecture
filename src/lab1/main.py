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
