"""Tests for all models in picks.models.py
Each model is tested in its own seperate class.
"""

from django.test import TestCase
from picks.models import Pick, Game, Team, Participant
from django.contrib.auth.models import User



class PickModelTest(TestCase):
    """Tests for the Pick Model in picks.models
    """
    @classmethod
    def setUpTestData(cls):
        # Setup for whole class - nothing should change these values.
        team1 = Team.objects.create(name='Oregon')
        team2 = Team.objects.create(name='Texas Tech')
        user = User.objects.create(username='Harry', password='nachocheese')
        parti = Participant.objects.create(name='LaKeith',user=user,is_self=False)
        # parti2 - goes with the second pick we make (planning on making game+participant to be unique).
        parti2 = Participant.objects.create(name='Johan',user=user,is_self=False)
        game = Game.objects.create(bowl='Rose Bowl', team1=team1, team2=team2, date='2023-12-28')
        Pick.objects.create(game=game, winner=team1, winby=12, owner=parti)
        # An incomplete pick to test __str__
        Pick.objects.create(game=game, winner=None, winby=None, owner=parti2)

    def test_game_label(self):
        pick = Pick.objects.get(id=1)
        field_label = pick._meta.get_field('game').verbose_name
        self.assertEqual(field_label, 'game')

    def test_winner_label(self):
        pick = Pick.objects.get(id=1)
        field_label = pick._meta.get_field('winner').verbose_name
        self.assertEqual(field_label, 'winner')

    def test_winby_label(self):
        pick = Pick.objects.get(id=1)
        field_label = pick._meta.get_field('winby').verbose_name
        self.assertEqual(field_label, 'winby')

    def test_owner_label(self):
        pick = Pick.objects.get(id=1)
        field_label = pick._meta.get_field('owner').verbose_name
        self.assertEqual(field_label, 'owner')

    def test_str_pickid_bowlname_owner_winner_beats_loser_winby_name(self):
        pick = Pick.objects.get(id=1)
        loser = 'Texas Tech'
        expected_object_name = f'{pick.id} {pick.game.bowl}: {pick.owner.name} picks {pick.winner.name} beats {loser} by {pick.winby}'
        self.assertEqual(str(pick), expected_object_name)

    def test_str_when_not_complete(self):
        pick = Pick.objects.get(id=2)
        expected_str = f'{pick.id} {pick.game.bowl}: {pick.owner.name} has not made a pick yet.'
        self.assertEquals(str(pick), expected_str)
    
    def test_get_loser(self):
        pick = Pick.objects.get(id=1)
        expected_loser = 'Texas Tech'
        self.assertEqual(pick.get_loser().name,expected_loser)



class GameModelTest(TestCase):
    """Tests for the Game model from picks.models
    """
    @classmethod
    def setUpTestData(cls):
        # Setup for whole class - nothing should change these values.
        team1 = Team.objects.create(name='Oregon')
        team2 = Team.objects.create(name='Texas Tech')
        Game.objects.create(bowl='Rose Bowl', team1=team1, team2=team2, date='2023-12-28')
    
    def test_bowl_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('bowl').verbose_name
        self.assertEqual(field_label, 'bowl')

    def test_date_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('date').verbose_name
        self.assertEqual(field_label, 'date')

    def test_team1_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('team1').verbose_name
        self.assertEquals(field_label, 'team1')
    
    def test_team2_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('team2').verbose_name
        self.assertEquals(field_label, 'team2')

    def test_team1_score_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('team1_score').verbose_name
        self.assertEquals(field_label, 'Team 1 Score')
    
    def test_team2_score_label(self):
        game = Game.objects.get(id=1)
        field_label = game._meta.get_field('team2_score').verbose_name
        self.assertEquals(field_label, 'Team 2 Score')
    
    def test_str_(self):
        game = Game.objects.get(id=1)
        expected_str = f'{game.bowl}: {game.team1} vs {game.team2} @ {game.date}'
        self.assertEquals(str(game), expected_str)



class ParticipantModelTest(TestCase):
    """Tests for the Participant model in picks.models
    """
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(username='harry', password='nachocheese')
        Participant.objects.create(name='lakeith',user=user,is_self=False)
        
    def test_name_label(self):
        participant = Participant.objects.get(id=1)
        field_label = participant._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_name_label(self):
        participant = Participant.objects.get(id=1)
        field_label = participant._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_name_label(self):
        participant = Participant.objects.get(id=1)
        field_label = participant._meta.get_field('is_self').verbose_name
        self.assertEquals(field_label, 'is self')

    def test_first_name_max_length(self):
        participant = Participant.objects.get(id=1)
        max_length = participant._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)



class TeamModelTest(TestCase):
    """Tests for the Team model from picks.models
    """
    @classmethod
    def setUpTestData(cls):
        Team.objects.create(name='Oregon')

    def test_name_label(self):
        team = Team.objects.get(id=1)
        field_label = team._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_first_name_max_length(self):
        team = Team.objects.get(id=1)
        max_length = team._meta.get_field('name').max_length
        self.assertEqual(max_length, 30)

    def test_str(self):
        team = Team.objects.get(id=1)
        self.assertEquals(str(team), 'Oregon')