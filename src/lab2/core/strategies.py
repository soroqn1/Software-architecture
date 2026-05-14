from abc import ABC, abstractmethod


class IMovementStrategy(ABC):
    @abstractmethod
    def move(self, animal_name: str, is_hungry: bool) -> str:
        pass


class RunStrategy(IMovementStrategy):
    def move(self, animal_name: str, is_hungry: bool) -> str:
        if is_hungry:
            return f"{animal_name} занадто голодний, щоб бігти, лише повільно повзе."
        return f"{animal_name} швидко біжить!"


class FlyStrategy(IMovementStrategy):
    def move(self, animal_name: str, is_hungry: bool) -> str:
        if is_hungry:
            return f"{animal_name} занадто голодна, щоб летіти, лише ходить по землі."
        return f"{animal_name} розправляє крила і злітає!"


class CrawlStrategy(IMovementStrategy):
    def move(self, animal_name: str, is_hungry: bool) -> str:
        if is_hungry:
            return f"{animal_name} повзе дуже повільно через голод."
        return f"{animal_name} впевнено повзе."
