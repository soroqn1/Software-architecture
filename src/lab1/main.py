from datetime import datetime, timedelta
from models import Dog, Lizard, Location, Owl
from owner import Owner


if __name__ == "__main__":
    owner = Owner("Петро")
    dog = Dog("собака")
    owl = Owl("сова")
    lizard = Lizard("ящіка")

    owner.add_animal(dog)
    owner.add_animal(owl)

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
