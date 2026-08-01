from catch_the_apple import config
from catch_the_apple.input import InputState
from catch_the_apple.math2d import clamp
from catch_the_apple.world import World


def update_movement(world: World, input_state: InputState, delta_time: float) -> None:
    basket = world.basket

    if input_state.left_pressed and basket.x > 0:
        basket.x -= basket.speed * delta_time
    if input_state.right_pressed and basket.x < config.SCREEN_WIDTH - basket.width:
        basket.x += basket.speed * delta_time

    basket.x = clamp(basket.x, 0, config.SCREEN_WIDTH - basket.width)

    for falling_object in world.falling_objects:
        falling_object.y += falling_object.speed * delta_time
