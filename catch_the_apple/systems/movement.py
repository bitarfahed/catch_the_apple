from catch_the_apple import config
from catch_the_apple.input import InputState
from catch_the_apple.math2d import clamp
from catch_the_apple.world import World


def update_movement(world: World, input_state: InputState, delta_time: float) -> None:
    update_basket_movement(world, input_state, delta_time)

    for falling_object in world.falling_objects:
        falling_object.previous_position.update(falling_object.transform.position)
        falling_object.y += falling_object.speed * delta_time


def update_basket_movement(world: World, input_state: InputState, delta_time: float) -> None:
    basket = world.basket
    movement = basket.movement

    movement.dash_cooldown_remaining = max(0.0, movement.dash_cooldown_remaining - delta_time)
    movement.dash_time_remaining = max(0.0, movement.dash_time_remaining - delta_time)

    input_direction = int(input_state.right_pressed) - int(input_state.left_pressed)
    dash_direction = get_dash_direction(input_direction, movement.direction.x, movement.velocity.x)
    if input_state.dash_pressed and dash_direction != 0.0 and movement.dash_cooldown_remaining <= 0.0:
        movement.dash_time_remaining = basket.dash_duration
        movement.dash_cooldown_remaining = basket.dash_cooldown
        movement.dash_direction = dash_direction

    if movement.is_dashing:
        movement.acceleration.update(0.0, 0.0)
        movement.velocity.x = movement.dash_direction * basket.dash_speed
    else:
        movement.acceleration.x = input_direction * basket.acceleration_rate
        movement.acceleration.y = 0.0
        movement.velocity.x += movement.acceleration.x * delta_time

        if input_direction == 0:
            movement.velocity.x = apply_drag(movement.velocity.x, basket.drag, delta_time)

        movement.velocity.x = clamp(movement.velocity.x, -basket.max_speed, basket.max_speed)

    basket.x += movement.velocity.x * delta_time

    min_x = 0.0
    max_x = config.SCREEN_WIDTH - basket.width
    basket.x = clamp(basket.x, min_x, max_x)
    if basket.x in (min_x, max_x) and is_moving_out_of_bounds(basket.x, movement.velocity.x, min_x, max_x):
        movement.velocity.x = 0.0

    movement.direction.x = get_motion_direction(movement.velocity.x)
    movement.direction.y = 0.0


def apply_drag(velocity: float, drag: float, delta_time: float) -> float:
    if velocity > 0.0:
        return max(0.0, velocity - drag * delta_time)
    if velocity < 0.0:
        return min(0.0, velocity + drag * delta_time)
    return 0.0


def is_moving_out_of_bounds(position: float, velocity: float, min_x: float, max_x: float) -> bool:
    return (position <= min_x and velocity < 0.0) or (position >= max_x and velocity > 0.0)


def get_dash_direction(input_direction: int, movement_direction: float, velocity: float) -> float:
    if input_direction != 0:
        return float(input_direction)
    if movement_direction != 0.0:
        return movement_direction
    return get_motion_direction(velocity)


def get_motion_direction(velocity: float) -> float:
    if velocity > 0.0:
        return 1.0
    if velocity < 0.0:
        return -1.0
    return 0.0
