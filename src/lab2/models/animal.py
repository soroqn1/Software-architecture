from datetime import datetime, timedelta
from enum import Enum
from src.lab2.core.events import Event, DeathEventArgs, HungerEventArgs, HappyEventArgs, AnimalEventArgs
from src.lab2.core.strategies import IMovementStrategy


class Location(Enum):
    OWNER = "Хазяїн"
    PET_SHOP = "Зоомагазин"
    WILD = "Воля"


class Animal:
    def __init__(self, name: str, paws: int, wings: int, movement_strategy: IMovementStrategy):
        self._name = name
        self._eyes = 2
        self._paws = paws
        self._wings = wings
        self._movement_strategy = movement_strategy

        self._location = Location.WILD
        self._last_meal_time = datetime.now()
        self._last_clean_time = datetime.now()
        self._meals_today = 0
        self._is_alive = True

        self.on_died = Event()
        self.on_hungry = Event()
        self.on_happy = Event()
        self.on_action = Event()

    @property
    def name(self) -> str:
        return self._name

    @property
    def paws(self) -> int:
        return self._paws

    @property
    def wings(self) -> int:
        return self._wings

    @property
    def location(self) -> Location:
        return self._location

    @location.setter
    def location(self, value: Location):
        self._location = value

    @property
    def is_alive(self) -> bool:
        return self._is_alive

    @property
    def is_hungry(self) -> bool:
        hours_since_meal = (datetime.now() - self._last_meal_time).total_seconds() / 3600
        return hours_since_meal >= 8

    def eat(self):
        if not self._is_alive:
            return
        
        if self._meals_today >= 5:
            self.on_action.emit(self, AnimalEventArgs(self, f"{self.name} не може більше їсти (ліміт 5 разів на день)."))
            return

        self._last_meal_time = datetime.now()
        self._meals_today += 1
        self.on_action.emit(self, AnimalEventArgs(self, f"{self.name} поїв(ла). Всього за сьогодні: {self._meals_today}"))

    def move(self):
        if not self._is_alive:
            self.on_action.emit(self, AnimalEventArgs(self, f"{self.name} мертвий(а) і не може рухатися."))
            return
        
        result = self._movement_strategy.move(self.name, self.is_hungry)
        self.on_action.emit(self, AnimalEventArgs(self, result))

    def clean(self):
        if not self._is_alive:
            return
        self._last_clean_time = datetime.now()
        self.on_action.emit(self, AnimalEventArgs(self, f"{self.name} тепер чистий(а)."))

    def _die(self, reason: str):
        self._is_alive = False
        self.on_died.emit(self, DeathEventArgs(self, f"{self.name} помер(ла) через {reason}."))

    def update_status(self):
        if not self._is_alive:
            return

        now = datetime.now()
        hours_since_meal = (now - self._last_meal_time).total_seconds() / 3600
        hours_since_clean = (now - self._last_clean_time).total_seconds() / 3600

        if hours_since_meal >= 24:
            self._die("голод (більше 24 годин без їжі)")
            return

        if hours_since_meal >= 8:
            self.on_hungry.emit(self, HungerEventArgs(self, f"{self.name} хоче їсти!"))

        if self.location == Location.WILD or hours_since_clean <= 24:
            self.on_happy.emit(self, HappyEventArgs(self, f"{self.name} почувається щасливим(ою)."))

    def simulate_time_pass(self, hours: float):
        if not self._is_alive:
            return
            
        self._last_meal_time -= timedelta(hours=hours)
        self._last_clean_time -= timedelta(hours=hours)
        
        days_passed = int(hours // 24)
        if days_passed > 0:
            self._meals_today = 0
