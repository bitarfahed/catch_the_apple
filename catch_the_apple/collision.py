from catch_the_apple.entities import Basket, FallingObject


def collides(basket: Basket, falling_object: FallingObject) -> bool:
    return basket.rect.colliderect(falling_object.rect)
