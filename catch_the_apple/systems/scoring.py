from catch_the_apple.session import GameSession


def add_score(session: GameSession) -> None:
    session.score += 1


def lose_life(session: GameSession) -> None:
    session.lives -= 1
