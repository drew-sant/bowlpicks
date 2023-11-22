from django.test import TestCase
from django.utils import timezone
import datetime

from picks.forms import EditPicksForm, AddGameForm, AddTeamForm, RegisterUserForm, AddParticipantForm, AddScoreForm
from picks.models import Team, Game, Participant, Pick
from django.contrib.auth.models import User

class EditPicksFormTest(TestCase):
    def setUp(self):
        # Create teams
        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')
        # Create game
        game = Game.objects.create(bowl='game1', team1=team1, team2=team2, date='2023-12-26')
        # Create user
        user = User.objects.create_user(username='user1', password='nachocheese')
        # Create participant
        part = Participant.objects.create(name='part1', user=user, is_self=False)
        # Create pick
        Pick.objects.create(game=game, winner=team1, winby=12, owner=part)

    def test_field_label(self):
        form = EditPicksForm(pickid=1)
        self.assertTrue(form.fields['winner'].label is None or form.fields['winner'].label == 'Winner')
        self.assertTrue(form.fields['winby'].label is None or form.fields['winby'].label == 'Win By')



class AddGameFormTest(TestCase):
    def test_field_label(self):
        form = AddGameForm()
        self.assertTrue(form.fields['bowl'].label is None or form.fields['bowl'].label == 'Bowl')
        self.assertTrue(form.fields['team1'].label is None or form.fields['team1'].label == 'Team1')
        self.assertTrue(form.fields['team2'].label is None or form.fields['team2'].label == 'Team2')
        self.assertTrue(form.fields['date'].label is None or form.fields['date'].label == 'Date')



class AddTeamFormTest(TestCase):
    def test_field_label(self):
        form = AddTeamForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')



class RegisterUserFormTest(TestCase):
    def test_field_label(self):
        form = RegisterUserForm()
        self.assertTrue(form.fields['username'].label is None or form.fields['username'].label == 'Username')
        self.assertTrue(form.fields['password'].label is None or form.fields['password'].label == 'Password')
        self.assertTrue(form.fields['password2'].label is None or form.fields['password2'].label == 'Password Again')
        self.assertTrue(form.fields['groupcode'].label is None or form.fields['groupcode'].label == 'Group Code')



class AddParticipantFormTest(TestCase):
    def test_field_label(self):
        form = AddParticipantForm()
        self.assertTrue(form.fields['name'].label is None or form.fields['name'].label == 'Name')

class AddScoreFormTest(TestCase):
    def test_field_label(self):
        form = AddScoreForm()
        self.assertTrue(form.fields['team1_score'].label is None or form.fields['team1_score'].label == 'Team 1 Score')
        self.assertTrue(form.fields['team2_score'].label is None or form.fields['team2_score'].label == 'Team 2 Score')