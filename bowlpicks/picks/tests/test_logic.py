"""Tests for the logic.py file.
"""

from django.test import TestCase
from picks.models import Game, Pick, Team, Participant, User
from picks.logic import scoreGroup

class TestScoreGroup(TestCase):
    def setUp(self):
        user = User.objects.create(username='user', password='nachocheese')
        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')

        game = Game.objects.create(bowl='game1', team1=team1, team2=team2, date='2023-12-26', team1_score=21, team2_score=9)
        winnersby = [(0, True, 4), (1, True, 3), (2, True, 12), (3, True, 11), (4, False, 13), (5, False, 11), (6, False, 7)]
        
        participants = []
        for x in range(len(winnersby)):
            participants.append(Participant.objects.create(name=f'part{winnersby[0]}', user=user, is_self=False))
        
        # team1 wins by 12 - one person gets it correct
        score = [1, 1, 3, 1, 0, 0, 0]
        for x in winnersby:
            part = participants[x[0]]
            if x[1]:
                Pick.objects.create(owner=part, winner=team1, winby=x[2], game=game)
            else:
                Pick.objects.create(owner=part, winner=team2, winby=x[2], game=game)
        
        # team 2 wins by 7 - two pick winby 7 and only one has it for the correct team
        addScore = [1, 1, 3, 1, 0, 0, 0]
        score = [x+y for x, y in zip(score, addScore)]
        game = Game.objects.create(bowl='game2', team1=team1, team2=team2, date='2023-12-26', team1_score=10, team2_score=17)
        winnersby = [(0, True, 31), (1, False, 1), (2, True, 10), (3, False, 5), (4, True, 14), (5, False, 7), (6, True, 7)]
        for x in winnersby:
            part = participants[x[0]]
            if x[1]:
                Pick.objects.create(owner=part, winner=team1, winby=x[2], game=game)
            else:
                Pick.objects.create(owner=part, winner=team2, winby=x[2], game=game)
        
        # team 2 wins by 20 - no one gets it exactly
        game = Game.objects.create(bowl='game3', team1=team1, team2=team2, date='2023-12-26', team1_score=3, team2_score=23)
        winnersby = [(0, True, 31), (1, False, 1), (2, True, 10), (3, False, 5), (4, True, 14), (5, False, 7), (6, True, 7)]
        for x in winnersby:
            part = participants[x[0]]
            if x[1]:
                Pick.objects.create(owner=part, winner=team1, winby=x[2], game=game)
            else:
                Pick.objects.create(owner=part, winner=team2, winby=x[2], game=game)
        
        # Three of the same winby with two of them picking winner.
        game = Game.objects.create(bowl='game3', team1=team1, team2=team2, date='2023-12-26', team1_score=14, team2_score=23)
        winnersby = [(0, True, 31), (1, False, 1), (2, True, 10), (3, False, 9), (4, True, 14), (5, False, 9), (6, True, 9)]
        for x in winnersby:
            part = participants[x[0]]
            if x[1]:
                Pick.objects.create(owner=part, winner=team1, winby=x[2], game=game)
            else:
                Pick.objects.create(owner=part, winner=team2, winby=x[2], game=game)
        
        # team1 wins by 3 - no one even picks the right team
        game = Game.objects.create(bowl='game3', team1=team1, team2=team2, date='2023-12-26', team1_score=3, team2_score=0)
        winnersby = [(0, False, 3), (1, False, 3), (2, False, 100), (3, False, 504), (4, False, 14), (5, False, 7), (6, False, 1)]
        for x in winnersby:
            part = participants[x[0]]
            if x[1]:
                Pick.objects.create(owner=part, winner=team1, winby=x[2], game=game)
            else:
                Pick.objects.create(owner=part, winner=team2, winby=x[2], game=game)

    def test_right_score_exact(self):
        correct_scores = [1, 1, 3, 1, 0, 0, 0]
        self.assertEqual(scoreGroup(), correct_scores)

    def test():
        pass