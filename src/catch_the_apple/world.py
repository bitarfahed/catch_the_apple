from dataclasses import dataclass, field

from catch_the_apple.entities import Basket, FallingObject


@dataclass
class World:
    basket: Basket = field(default_factory=Basket)
    falling_objects: list[FallingObject] = field(default_factory=list)

    def add_falling_object(self, falling_object: FallingObject) -> None:
        self.falling_objects.append(falling_object)

    def remove_falling_object(self, falling_object: FallingObject) -> None:
        self.falling_objects.remove(falling_object)
