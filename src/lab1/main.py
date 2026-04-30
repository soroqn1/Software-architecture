from datetime import datetime, timedelta
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

        self.is_happy = []

        self.last_clean_time = datetime.now()

    def eat(self):
        if self.meals_today < 5:
            self.last_meal_time = datetime.now()
            self.meals_today += 1
            print(f"{self.name} поїв")

    def move(self):
        hours = (datetime.now() - self.last_meal_time).total_seconds() / 3600
        if hours >= 8:
            print(f"{self.name} занадто голодний, щоб бігти, тільки повзе")
        else:
            print(f"{self.name} бадьоро біжить")

    def clean(self):
        self.last_clean_time = datetime.now()
        self.is_cleaned = True
        print(f"{self.name} чистий")

    def fly(self):
        if self.wings == 0:
            print(f"{self.name} не має крил, щоб літати")
            return

        hours = (datetime.now() - self.last_meal_time).total_seconds() / 3600
        if hours >= 8:
            print(f"{self.name} занадто голодна сова, щоб летіти")
        else:
            print(f"{self.name} розправив крила і злетів")

    def release_to_wild(self):
        self.location = Location.WILD
        print(f"{self.name} тепер на волі")

    def check_status(self):
        hours_since_cleaning = (
            datetime.now() - self.last_clean_time
        ).total_seconds() / 3600
        hours_since_meal = (datetime.now() - self.last_meal_time).total_seconds() / 3600

        if not self.is_alive:
            return

        if hours_since_meal >= 24:
            self.is_alive = False
            for callback in self.on_died:
                callback(self)
        elif hours_since_meal >= 8:
            for callback in self.on_hungry:
                callback(self)
        if (
            hours_since_meal <= 8
            and hours_since_cleaning <= 24
            or self.location == Location.WILD
        ):
            for callback in self.is_happy:
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


if __name__ == "__main__":
    dog = Dog("собака")
    owl = Owl("сова")
    lizard = Lizard("ящіка")

    def handle_death(a):
        print(f"ПОДІЯ: {a.name} помер від голоду")

    def handle_hunger(a):
        print(f"ПОДІЯ: {a.name} дуже хоче їсти")

    def handle_happy(a):
        print(f"ПОДІЯ: {a.name} почувається щасливим")

    for a in [dog, owl]:
        a.on_died.append(handle_death)
        a.on_hungry.append(handle_hunger)
        a.is_happy.append(handle_happy)

    print("анатомія")
    print(f"{dog.name}: лап {dog.paws}, крил {dog.wings}")
    print(f"{owl.name}: лап {owl.paws}, крил {owl.wings}")
    dog.move()
    owl.fly()
    dog.fly()

    print("голод")
    dog.last_meal_time = datetime.now() - timedelta(hours=9)
    dog.check_status()
    dog.move()
    owl.last_meal_time = datetime.now() - timedelta(hours=9)
    owl.fly()

    print("прибирання")
    dog.location = Location.OWNER
    dog.last_clean_time = datetime.now() - timedelta(hours=25)
    print("до прибирання")
    dog.check_status()
    dog.clean()
    print("після прибирання")
    dog.check_status()

    print("смерть")
    owl.last_meal_time = datetime.now() - timedelta(hours=25)
    owl.check_status()
    print(f"Живий? {owl.is_alive}")

    print("воля")
    lizard.location = Location.WILD
    print(f"{lizard.name} на волі, перевіряємо щастя")
    lizard.check_status()
