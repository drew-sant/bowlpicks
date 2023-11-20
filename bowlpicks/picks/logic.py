"""A module that provides functions that takes care of logic for the app."""

from picks.models import Game, Pick

# 1 point for correct winner
# 2 points for being the closest with an additional point if exact
# correct winner plus 1
# closest plus 1
# exact plus 1

def scoreGroup() -> list[tuple]:
    """Return a list of tuples that contain a participant's id, their name, and their overall score."""
    # get the group picks
    # variable for closest (smallest difference value)
    # loop through each game's picks
        # plus 1 for correct winner
        # if better than closest then update closest value
    # get list of all participants with winby (reversed with )
    # plus 1 for closest
    # plus 1 for exact
    # output a list of tuples in the form of [(participant_id, score)]
    # l = [(0,)]
    # num = 0
    # l.index([x for x in l if num in x][0])
    return [(None, None)]

def scoreGame(picks: dict) -> list[tuple]:
    """Return a list of tuples of each participant's scores
    [(participant_id, score)]
    """
    return [(None, None)]

def getAllGameScore() -> dict:
    """Return a dictionary of the game name, score of team1, and score of team2
    """
    return {}

def getGroupPicksByGame() -> dict:
    """Return a dictionary with each game and the participant's picks for each game.
    {'bowlgame1':
        {'participant1':
            {'winner': Team, 'winby' int},
        },
        ...
    }
    """
    return {}