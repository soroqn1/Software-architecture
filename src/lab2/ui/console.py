import sys
from typing import List, Optional
from src.lab2.models.animal import Animal, Location
from src.lab2.models.owner import Owner
from src.lab2.core.factory import AnimalFactory
from src.lab2.core.events import AnimalEventArgs, DeathEventArgs, HungerEventArgs, HappyEventArgs


class ConsoleUI:
    def __init__(self):
        self.owner: Optional[Owner] = None
        self.all_animals: List[Animal] = []

    def start(self):
        print("=== Система управління тваринами ===")
        name = input("Введіть ім'я господаря: ")
        self.owner = Owner(name)
        
        while True:
            self._display_menu()
            choice = input("\nОберіть дію: ").strip()
            
            try:
                if choice == "1":
                    self._add_animal()
                elif choice == "2":
                    self._list_animals()
                elif choice == "3":
                    self._feed_animal()
                elif choice == "4":
                    self._clean_animal()
                elif choice == "5":
                    self._move_animal()
                elif choice == "6":
                    self._simulate_time()
                elif choice == "7":
                    self._check_status()
                elif choice == "0":
                    print("Вихід...")
                    break
                else:
                    print("Невірний вибір.")
            except Exception as e:
                print(f"Помилка: {e}")

    def _display_menu(self):
        print("\n--- Меню ---")
        print("1. Додати/Прихистити тварину")
        print("2. Список моїх тварин")
        print("3. Нагодувати тварину")
        print("4. Почистити за твариною")
        print("5. Змусити тварину рухатися")
        print("6. Симулювати проходження часу")
        print("7. Перевірити стан усіх")
        print("0. Вихід")

    def _add_animal(self):
        print(f"Доступні типи: {', '.join(AnimalFactory.get_available_types())}")
        atype = input("Тип: ").lower()
        aname = input("Ім'я: ")
        
        animal = AnimalFactory.create_animal(atype, aname)
        self.all_animals.append(animal)

        animal.on_died.subscribe(self._handle_event)
        animal.on_hungry.subscribe(self._handle_event)
        animal.on_happy.subscribe(self._handle_event)
        animal.on_action.subscribe(self._handle_event)
        
        adopt = input("Прихистити цю тварину? (т/н): ").lower()
        if adopt == 'т':
            self.owner.adopt_animal(animal)
            print(f"{aname} тепер під опікою {self.owner.name}.")
        else:
            print(f"{aname} залишається на волі.")

    def _list_animals(self):
        if not self.owner.animals:
            print("У вас немає тварин.")
            return
        
        print("\nВаші тварини:")
        for i, a in enumerate(self.owner.animals):
            status = "Живий(а)" if a.is_alive else "Мертвий(а)"
            print(f"{i+1}. {a.name} ({a.__class__.__name__}) - {status}")

    def _feed_animal(self):
        animal = self._select_animal()
        if animal:
            animal.eat()

    def _clean_animal(self):
        animal = self._select_animal()
        if animal:
            animal.clean()

    def _move_animal(self):
        animal = self._select_animal()
        if animal:
            animal.move()

    def _simulate_time(self):
        try:
            hours = float(input("Скільки годин має пройти: "))
            for a in self.all_animals:
                a.simulate_time_pass(hours)
                a.update_status()
            print(f"Минуло {hours} годин.")
        except ValueError:
            print("Невірне значення годин.")

    def _check_status(self):
        for a in self.all_animals:
            a.update_status()
            status = "Живий(а)" if a.is_alive else "Мертвий(а)"
            location = a.location.value
            print(f"[{a.name}] Стан: {status}, Місце: {location}")

    def _select_animal(self) -> Optional[Animal]:
        self._list_animals()
        if not self.owner.animals:
            return None
        
        try:
            idx = int(input("Оберіть номер тварини: ")) - 1
            if 0 <= idx < len(self.owner.animals):
                return self.owner.animals[idx]
        except ValueError:
            pass
        print("Невірний вибір.")
        return None

    def _handle_event(self, sender: Animal, args: AnimalEventArgs):
        prefix = "!!! ПОДІЯ !!!"
        if isinstance(args, DeathEventArgs):
            prefix = "СМЕРТЬ"
        elif isinstance(args, HungerEventArgs):
            prefix = "ГОЛОД"
        elif isinstance(args, HappyEventArgs):
            prefix = "ЩАСТЯ"
        elif isinstance(args, AnimalEventArgs):
            prefix = "ДІЯ"
            
        print(f"\n[{prefix}] {args.message}")
