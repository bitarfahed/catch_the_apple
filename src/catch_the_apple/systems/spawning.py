import random

from catch_the_apple import config
from catch_the_apple.entities import FallingObject
from catch_the_apple.math2d import Transform2D, vec2
from catch_the_apple.object_definitions import ObjectDefinition, get_spawnable_definitions
from catch_the_apple.world import World


class SpawnSystem:
    def __init__(self, spawn_config: config.SpawnConfig) -> None:
        self.config = spawn_config
        self.random = random.Random(spawn_config.seed)
        self.spawnable_definitions = get_spawnable_definitions(spawn_config.enabled_object_ids)

    def update(self, world: World) -> None:
        while len(world.falling_objects) < self.config.max_active_objects:
            world.add_falling_object(self.create_falling_object())

    def create_falling_object(self) -> FallingObject:
        definition = self.choose_object_definition()
        return FallingObject(
            transform=Transform2D(
                position=vec2(self.random_falling_object_x(definition), self.config.spawn_y)
            ),
            definition=definition,
            speed=self.config.object_speed,
        )

    def choose_object_definition(self) -> ObjectDefinition:
        return self.random.choices(
            self.spawnable_definitions,
            weights=[definition.spawn_weight for definition in self.spawnable_definitions],
            k=1,
        )[0]

    def reset_falling_object(self, falling_object: FallingObject) -> None:
        falling_object.x = self.random_falling_object_x(falling_object.definition)
        falling_object.y = self.config.spawn_y
        falling_object.previous_position.update(falling_object.transform.position)

    def random_falling_object_x(self, definition: ObjectDefinition) -> int:
        max_x = min(self.config.x_max, config.SCREEN_WIDTH - definition.collision_size)
        return self.random.randint(self.config.x_min, max_x)
