from catch_the_apple.session import GameSession


def add_score(session: GameSession, amount: int) -> None:
    session.score += amount
    session.combo += 1


def lose_life(session: GameSession, amount: int) -> None:
    session.lives -= amount
    session.combo = 0
