from enum import Enum

K = 30


class PlayerScore(Enum):
    LOSS = 0.0
    DRAW = 0.5
    WIN = 1.0


def reverse_score(score: PlayerScore) -> PlayerScore:
    if score == PlayerScore.LOSS:
        return PlayerScore.WIN
    elif score == PlayerScore.WIN:
        return PlayerScore.LOSS
    else:
        return score


def elo_change(elo1: int, elo2: int, player_score: PlayerScore) -> int:
    """
    Returns change of elo rating of player1.

    elo1 - current elo of player1
    elo2 - current elo of player2
    player_score - score of player1

    The caller of this method should add the returned value to player1's elo and subtract it from player2's elo to get
    the new elo ratings for both players.
    """
    expected_score = 1 / (1 + 10**((elo2 - elo1) / 400))
    change = K * (player_score.value - expected_score)
    return round(change)

