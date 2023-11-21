"""A module that provides functions that takes care of logic for the app."""

from picks.models import Game, Pick, Participant

import logging
logging = logging.getLogger(__name__)

# 1 point for correct winner
# 2 points for being the closest with an additional point if exact
# correct winner plus 1
# closest plus 1
# exact plus 1

def scoreGroup() -> list[tuple]:
    """Return a list of tuples that contain a participant's id, their name, and their overall score."""
    # get the group picks
    games = {}
    all_games = Game.objects.all().exclude(team1_score=None).exclude(team2_score=None)
    for game in all_games:
        game_query = Pick.objects.filter(game=game)
        d = []
        for pick in game_query:
            d.append((pick.owner.id, pick.winner, pick.winby))
        
        games[game.id] = {'game': game, 'picks':d}
    logging.debug(f'# of games read: {len(games)}')
    
    if games == {}:
        # If their are no games that have scores then return everyone with a score of 0
        parti = Participant.objects.all()
        return [(x.id, 0) for x in parti]

    # variable for closest (smallest difference value)
    participants_scores = {}
    for id, _, _ in games[list(games.keys())[0]]['picks']:
        participants_scores[id] = 0
    logging.debug(f'# of participants: {len(participants_scores)}')

    # loop through each game's picks
    for game in games:
        closestWinby = None
        for pick in games[game]['picks']:
            score = 0 # default score is 0
            id, winner, winby = pick # Decompose each pick

            team1 = games[game]['game'].team1
            team2 = games[game]['game'].team2
            team1_score = games[game]['game'].team1_score
            team2_score = games[game]['game'].team2_score

            if winner == (team1 if team1_score > team2_score else team2):
                # If picked winner then plus one
                score = score + 1
                closestWinby = winby if closestWinby == None else closestWinby

                score_diff = abs(team1_score - team2_score)

                if abs(winby - score_diff) < abs(closestWinby - score_diff):
                    # if better than closest then update closest value
                    logging.debug(f'closestWinby updated from: {closestWinby} to {winby}')
                    closestWinby = winby
            
            participants_scores[id] = participants_scores[id] + score
        plus = [id for (id, winner, winby) in games[game]['picks'] if winby == closestWinby and winner == (team1 if team1_score > team2_score else team2)]
        if closestWinby == abs(games[game]['game'].team1_score - games[game]['game'].team2_score):
            for id in plus:
                participants_scores[id] = participants_scores[id] + 2
        else:
            for id in plus:
                participants_scores[id] = participants_scores[id] + 1
    list_scores = [(id, score) for id, score in participants_scores.items()]
    # output a list of tuples in the form of [(participant_id, score)]
    return list_scores

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