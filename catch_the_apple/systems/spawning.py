import random

from catch_the_apple import config
from catch_the_apple.entities import FallingObject
from catch_the_apple.math2d import Transform2D, vec2
from catch_the_apple.world import World


class SpawnSystem:
    def __init__(self, spawn_config: config.SpawnConfig) -> None:
        self.config = spawn_config
        self.random = random.Random(spawn_config.seed)

    def update(self, world: World) -> None:
        while len(world.falling_objects) < self.config.max_active_objects:
            world.add_falling_object(self.create_regular_apple())

    def create_regular_apple(self) -> FallingObject:
        return FallingObject(
            transform=Transform2D(position=vec2(self.random_falling_object_x(), self.config.spawn_y)),
            size=self.config.object_size,
            speed=self.config.object_speed,
        )

    def reset_falling_object(self, falling_object: FallingObject) -> None:
        falling_object.x = self.random_falling_object_x()
        falling_object.y = self.config.spawn_y

    def random_falling_object_x(self) -> int:
        return self.random.randint(self.config.x_min, self.config.x_max)
