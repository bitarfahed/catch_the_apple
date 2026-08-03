from dataclasses import dataclass

import pygame

from catch_the_apple.entities import Basket, FallingObject


@dataclass(frozen=True)
class CircleShape:
    center: pygame.Vector2
    radius: float


@dataclass(frozen=True)
class BasketCollisionModel:
    catch_region: pygame.Rect
    left_rim: pygame.Rect
    right_rim: pygame.Rect
    body: pygame.Rect


@dataclass(frozen=True)
class CollisionResult:
    caught: bool = False
    hit_left_rim: bool = False
    hit_right_rim: bool = False
    hit_body: bool = False
    used_ccd: bool = False

    @property
    def collided(self) -> bool:
        return self.caught or self.hit_left_rim or self.hit_right_rim or self.hit_body


def build_basket_collision_model(basket: Basket) -> BasketCollisionModel:
    return BasketCollisionModel(
        catch_region=basket.catch_region_rect,
        left_rim=basket.left_rim_rect,
        right_rim=basket.right_rim_rect,
        body=basket.body_rect,
    )


def build_object_circle(falling_object: FallingObject) -> CircleShape:
    return CircleShape(center=falling_object.center, radius=falling_object.radius)


def detect_basket_collision(basket: Basket, falling_object: FallingObject) -> CollisionResult:
    model = build_basket_collision_model(basket)
    circle = build_object_circle(falling_object)

    caught = circle_intersects_rect(circle, model.catch_region)
    hit_left_rim = circle_intersects_rect(circle, model.left_rim)
    hit_right_rim = circle_intersects_rect(circle, model.right_rim)
    hit_body = circle_intersects_rect(circle, model.body)

    used_ccd = False
    if not caught:
        caught = swept_circle_intersects_rect(
            falling_object.previous_center,
            falling_object.center,
            falling_object.radius,
            model.catch_region,
        )
        used_ccd = caught

    return CollisionResult(
        caught=caught,
        hit_left_rim=hit_left_rim,
        hit_right_rim=hit_right_rim,
        hit_body=hit_body,
        used_ccd=used_ccd,
    )


def collides(basket: Basket, falling_object: FallingObject) -> bool:
    return detect_basket_collision(basket, falling_object).caught


def circle_intersects_rect(circle: CircleShape, rect: pygame.Rect) -> bool:
    closest_x = max(rect.left, min(circle.center.x, rect.right))
    closest_y = max(rect.top, min(circle.center.y, rect.bottom))
    distance_squared = (circle.center.x - closest_x) ** 2 + (circle.center.y - closest_y) ** 2
    return distance_squared <= circle.radius**2


def swept_circle_intersects_rect(
    start: pygame.Vector2,
    end: pygame.Vector2,
    radius: float,
    rect: pygame.Rect,
) -> bool:
    expanded = rect.inflate(radius * 2, radius * 2)
    return segment_intersects_rect(start, end, expanded)


def segment_intersects_rect(start: pygame.Vector2, end: pygame.Vector2, rect: pygame.Rect) -> bool:
    if rect.collidepoint(start.x, start.y) or rect.collidepoint(end.x, end.y):
        return True

    direction = end - start
    t_min = 0.0
    t_max = 1.0

    for axis in ("x", "y"):
        axis_direction = getattr(direction, axis)
        axis_start = getattr(start, axis)
        axis_min = getattr(rect, "left" if axis == "x" else "top")
        axis_max = getattr(rect, "right" if axis == "x" else "bottom")

        if axis_direction == 0.0:
            if axis_start < axis_min or axis_start > axis_max:
                return False
            continue

        inverse_direction = 1.0 / axis_direction
        t1 = (axis_min - axis_start) * inverse_direction
        t2 = (axis_max - axis_start) * inverse_direction
        if t1 > t2:
            t1, t2 = t2, t1

        t_min = max(t_min, t1)
        t_max = min(t_max, t2)
        if t_min > t_max:
            return False

    return True
