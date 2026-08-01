from catch_the_apple.entities import Apple, Basket


def collides(basket: Basket, apple: Apple) -> bool:
    return basket.rect.colliderect(apple.rect)
