from catch_the_apple.session import GameSession


def add_score(session: GameSession, amount: int) -> None:
    session.score += amount
    if amount > 0:
        session.has_earned_score = True
    session.combo += 1
    session.best_combo = max(session.best_combo, session.combo)


def subtract_score(session: GameSession, amount: int) -> None:
    session.score = max(0, session.score - amount)
    session.combo = 0


def lose_life(session: GameSession, amount: int) -> None:
    session.lives -= amount
    session.combo = 0
