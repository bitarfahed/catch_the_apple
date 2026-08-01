from dataclasses import dataclass, field

from catch_the_apple.entities import Apple, Basket
from catch_the_apple.systems.spawning import create_apple


@dataclass
class World:
    basket: Basket = field(default_factory=Basket)
    falling_objects: list[Apple] = field(default_factory=lambda: [create_apple()])

    @property
    def apple(self) -> Apple:
        return self.falling_objects[0]
