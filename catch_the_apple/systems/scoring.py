from catch_the_apple.session import GameSession


def add_score(session: GameSession, amount: int) -> None:
    session.score += amount


def lose_life(session: GameSession, amount: int) -> None:
    session.lives -= amount
