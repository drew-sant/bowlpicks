"""Tests for all views in picks.views.py
Each model is tested in its own seperate class.
"""
from django.test import TestCase
from django.urls import reverse
# from django.contrib.auth.mixins import LoginRequiredMixin

# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
User = get_user_model()

from picks.models import Pick, Game, Team, Participant
from picks.forms import EditPicksForm, AddParticipantForm, RegisterUserForm, AddGameForm, AddTeamForm, AddScoreForm

class EditPicksViewTest(TestCase):
    """Tests for edit picks view
    """

    def setUp(self):
        # Create users
        test_user1 = User.objects.create_user(username='user1', password = 'nachocheese')

        # Create teams
        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')
        # Create participant
        parti = Participant.objects.create(name='puser1',user=test_user1,is_self=True)
        # parti2 - goes with the second pick we make (planning on making game+participant to be unique).
        parti2 = Participant.objects.create(name='johan',user=test_user1,is_self=False)
        # Create game
        game = Game.objects.create(bowl='Rose Bowl', team1=team1, team2=team2, date='2023-12-28')
        # Create pick
        Pick.objects.create(game=game, winner=team1, winby=12, owner=parti) # url /1/1
        # An incomplete pick to test make sure it doesn't break anything
        Pick.objects.create(game=game, winner=None, winby=None, owner=parti2) # url /2/2

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/edit-picks/1/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/edit-picks/1/1')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/edit-picks/1/1')
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get(reverse('editPicks', kwargs={'userid': 1,'pickid':1}))
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/edit-picks/1/1')
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_picks.html')
    
    def test_view_has_form(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/edit-picks/1/1')
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], EditPicksForm)

    def test_incomplete_pick(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/edit-picks/2/2')
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)



class AccountViewTest(TestCase):
    def setUp(self):
        # Create users
        test_user1 = User.objects.create_user(username='user1', password = 'nachocheese')
        # Create participant
        parti = Participant.objects.create(name='puser1',user=test_user1,is_self=True)
        # parti2 - goes with the second pick we make (planning on making game+participant to be unique).
        parti2 = Participant.objects.create(name='johan',user=test_user1,is_self=False)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/account')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/account')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/account')
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get(reverse('account'))
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/account')
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'account.html')
    
    def test_view_has_form(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/account')
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddParticipantForm)

    def test_with_userid_sent(self):
        """See if a userid can be sent"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/account/1')
        self.assertEqual(response.status_code, 200)
    
    def test_view_has_list(self):
        """Make sure we are getting a list sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/account')
        self.assertIsInstance(response.context['linkedUsers'], list)



class GroupPicksViewTest(TestCase):
    def setUp(self):
        # Create users
        test_user1 = User.objects.create_user(username='user1', password = 'nachocheese')
        test_user2 = User.objects.create_user(username='user2', password = 'nachocheese')
        # Create participant
        parti1 = Participant.objects.create(name='puser1',user=test_user1,is_self=True)
        parti2 = Participant.objects.create(name='johan',user=test_user1,is_self=False)
        parti3 = Participant.objects.create(name='marc',user=test_user2,is_self=True)
        parti4 = Participant.objects.create(name='barney',user=test_user2,is_self=False)
        # Create Teams
        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')
        # Create Games
        game1 = Game.objects.create(bowl='game1', team1=team1, team2=team2, date='2023-12-26')
        # Create Picks
        Pick.objects.create(game=game1, winner=team1, winby=7, owner=parti1)
        Pick.objects.create(game=game1, winner=team2, winby=14, owner=parti2)
        Pick.objects.create(game=game1, winner=team1, winby=14, owner=parti3)
        Pick.objects.create(game=game1, winner=team2, winby=7, owner=parti4)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/group-picks/users')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/group-picks/users')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/users')
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get(reverse('groupPickslayout', kwargs={'layout': 'users'}))
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/users')
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'group_picks.html')

    def test_with_id_sent(self):
        """See if a game or user id can be sent"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/users/1')
        self.assertEqual(response.status_code, 200)
    
    def test_view_has_users_list(self):
        """Make sure we are getting a list of users sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/users')
        self.assertIsInstance(response.context['users'], list)
        self.assertEqual(len(response.context['users']), 4)

    def test_view_has_games_dict(self):
        """Make sure we are getting a list of games sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/games')
        self.assertIsInstance(response.context['games'], dict)
        self.assertEqual(len(response.context['games']), 4)

    def test_view_has_bowls_list(self):
        """Make sure we are getting a list of bowl games sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/users')
        self.assertIsInstance(response.context['bowls'], list)
        self.assertEqual(len(response.context['bowls']), 1)

    def test_view_has_picks_dict(self):
        """Make sure we are getting a list of picks sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/users')
        self.assertIsInstance(response.context['picks'], dict)
        self.assertEqual(len(response.context['picks']), 1)

    def test_view_has_layout_string(self):
        """Make sure we are getting a string indicating layout sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/users')
        self.assertIsInstance(response.context['layout'], str)

    def test_view_has_userorgame_participant(self):
        """Make sure we are getting a user or game sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/users')
        self.assertIsInstance(response.context['userorgame'], Participant)
    
    def test_view_has_userorgame_game(self):
        """Make sure we are getting a user or game sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/group-picks/games')
        self.assertIsInstance(response.context['userorgame'], int)



class MyPicksViewTest(TestCase):
    def setUp(self):
        # Create users
        test_user1 = User.objects.create_user(username='user1', password = 'nachocheese')
        test_user2 = User.objects.create_user(username='user2', password = 'nachocheese')
        # Create participant
        parti1 = Participant.objects.create(name='puser1',user=test_user1,is_self=True)
        parti2 = Participant.objects.create(name='johan',user=test_user1,is_self=False)
        parti3 = Participant.objects.create(name='marc',user=test_user2,is_self=True)
        parti4 = Participant.objects.create(name='barney',user=test_user2,is_self=False)
        # Create Teams
        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')
        # Create Games
        game1 = Game.objects.create(bowl='game1', team1=team1, team2=team2, date='2023-12-26')
        # Create Picks
        Pick.objects.create(game=game1, winner=team1, winby=7, owner=parti1)
        Pick.objects.create(game=game1, winner=team2, winby=14, owner=parti2)
        Pick.objects.create(game=game1, winner=team1, winby=14, owner=parti3)
        Pick.objects.create(game=game1, winner=team2, winby=7, owner=parti4)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get('/my-picks')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/my-picks')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/my-picks')
        self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get(reverse('myPicks'))
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_accessible_by_name_with_user_id(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get(reverse('myPicksid', kwargs={'user': 1}))
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/my-picks')
        # self.assertEqual(str(response.context['user']), 'user1')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_picks.html')

    def test_with_id_sent(self):
        
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/my-picks/1')
        self.assertEqual(response.status_code, 200)
    
    def test_view_has_linked_users_list(self):
        
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/my-picks/1')
        self.assertIsInstance(response.context['linked_users'], list)
        self.assertEqual(len(response.context['linked_users']), 2)

    def test_view_has_selected_user_tuple(self):
        
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/my-picks')
        self.assertIsInstance(response.context['selected'], tuple)
        self.assertEqual(len(response.context['selected']), 2)

    def test_view_has_picks_list(self):
        """Make sure we are getting a list of bowl games sent to the template"""
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/my-picks/1')
        self.assertIsInstance(response.context['picks'], list)
        self.assertEqual(len(response.context['picks']), 1)



class RegisterViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'register.html')
    
    def test_view_has_form(self):
        response = self.client.get('/register')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], RegisterUserForm)



class SetupViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_admin_user = User.objects.create_superuser(username='test_admin', password='nachocheese')
        test_user = User.objects.create(username='test_user', password='nachocheese')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/setup')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get(reverse('setup'))
        self.assertEqual(response.status_code, 200)

    def test_view_redirects_not_admin_user(self):
        login = self.client.login(username='test_user', password='nachocheese')
        response = self.client.get('/setup')
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_not_logged_in(self):
        response = self.client.get('/setup')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/setup')

    def test_view_uses_correct_template(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/setup')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'setup.html')
    
    def test_view_has_form(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/setup')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddGameForm)

    def test_view_has_game_list(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/setup')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['games'], list)



class AddTeamViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        test_admin_user = User.objects.create_superuser(username='test_admin', password='nachocheese')
        test_user = User.objects.create(username='test_user', password='nachocheese')

        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/addteam')
        self.assertEqual(response.status_code, 200)
    
    def test_view_url_with_id(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/addteam/1')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get(reverse('addteam'))
        self.assertEqual(response.status_code, 200)

    def test_view_redirects_not_admin_user(self):
        login = self.client.login(username='test_user', password='nachocheese')
        response = self.client.get('/addteam')
        self.assertEqual(response.status_code, 302)

    def test_view_redirects_not_logged_in(self):
        response = self.client.get('/addteam')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/addteam')

    def test_view_uses_correct_template(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/addteam')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_team.html')
    
    def test_view_has_form(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/addteam')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddTeamForm)

    def test_view_has_team_list(self):
        login = self.client.login(username='test_admin', password='nachocheese')
        response = self.client.get('/addteam')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['teams'], list)
        self.assertEqual(len(response.context['teams']), 2)



class DeleteParticipantViewTest(TestCase):
    def setUp(self):
        # Create users
        test_user1 = User.objects.create_user(username='user1', password = 'nachocheese')
        test_user2 = User.objects.create_user(username='user2', password = 'nachocheese')
        # Create participant
        parti1 = Participant.objects.create(name='puser1',user=test_user1,is_self=False)
        parti2 = Participant.objects.create(name='puser1',user=test_user1,is_self=True)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/deletepart/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account')
        self.assertNotEqual(response.content,
                            b"FAILED. Participant doesn't belong to current user or participant is self. <a href= '/account'>Back</a>")
    
    def test_view_logged_out(self):
        response = self.client.get('/deletepart/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/deletepart/1')
    
    def test_view_participant_does_not_belong_to_user(self):
        login = self.client.login(username='user2', password='nachocheese')
        response = self.client.get('/deletepart/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         b"FAILED. Participant doesn't belong to current user or participant is self. <a href= '/account'>Back</a>")

    def test_view_participant_is_self(self):
        login = self.client.login(username='user2', password='nachocheese')
        response = self.client.get('/deletepart/1')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content,
                         b"FAILED. Participant doesn't belong to current user or participant is self. <a href= '/account'>Back</a>")

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get(reverse('deletepart', kwargs={'userid': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/account')



class LogoutViewTest(TestCase):
    def setUp(self):
        # Create user
        test_user1 = User.objects.create_user(username='user1', password = 'nachocheese')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get('/logout')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        login = self.client.login(username='user1', password='nachocheese')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/logged_out.html') #



class DeleteTeamViewTest(TestCase):
    def setUp(self):
        # Create users
        User.objects.create_user(username='user', password = 'nachocheese')
        User.objects.create_superuser(username='admin', password = 'nachocheese')
        # Create teams
        Team.objects.create(name='team1')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='admin', password='nachocheese')
        response = self.client.get('/deleteteam/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/addteam')
    
    def test_view_logged_out(self):
        response = self.client.get('/deleteteam/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/deleteteam/1')
    
    def test_view_user_is_not_admin(self):
        login = self.client.login(username='user', password='nachocheese')
        response = self.client.get('/deleteteam/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/deleteteam/1')

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='admin', password='nachocheese')
        response = self.client.get(reverse('delete_team', kwargs={'teamid': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/addteam')



class DeleteGameViewTest(TestCase):
    def setUp(self):
        # Create users
        User.objects.create_user(username='user', password = 'nachocheese')
        User.objects.create_superuser(username='admin', password = 'nachocheese')
        # Create teams
        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')
        # Create game
        Game.objects.create(bowl='game1', team1=team1, team2=team2, date='2023-12-26')

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='admin', password='nachocheese')
        response = self.client.get('/deletegame/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/setup')
    
    def test_view_logged_out(self):
        response = self.client.get('/deletegame/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/deletegame/1')
    
    def test_view_user_is_not_admin(self):
        login = self.client.login(username='user', password='nachocheese')
        response = self.client.get('/deletegame/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/deletegame/1')

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='admin', password='nachocheese')
        response = self.client.get(reverse('delete_game', kwargs={'gameid': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/setup')



class LoginViewTest(TestCase):

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/login')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/login.html')



class AdminPageViewTest(TestCase):
    def setUp(self):
        # Create users
        User.objects.create_user(username='user', password = 'nachocheese')
        User.objects.create_superuser(username='admin', password = 'nachocheese')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='admin', password='nachocheese')
        response = self.client.get('/admin-page')
        self.assertEqual(response.status_code, 200)

    def test_view_not_logged_in(self):
        response = self.client.get('/admin-page')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=%2Fadmin-page')
    
    def test_view_not_admin(self):
        self.client.login(username='user', password='nachocheese')
        response = self.client.get('/admin-page')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=%2Fadmin-page')

    def test_view_url_accessible_by_name(self):
        self.client.login(username='admin', password='nachocheese')
        response = self.client.get(reverse('adminPage'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='admin', password='nachocheese')
        response = self.client.get(reverse('adminPage'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'admin_page.html')

class addScoringViewTest(TestCase):
    def setUp(self):
        # Create users
        User.objects.create_user(username='user', password = 'nachocheese')
        User.objects.create_superuser(username='admin', password = 'nachocheese')
        # Create teams
        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')
        # Create game
        Game.objects.create(bowl='game1', team1=team1, team2=team2, date='2023-12-26')

    def test_view_url_exists_at_desired_location(self):
        self.client.login(username='admin', password='nachocheese')
        response = self.client.get('/addscore/1')
        self.assertEqual(response.status_code, 200)

    def test_view_not_logged_in(self):
        response = self.client.get('/addscore/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/addscore/1')
    
    def test_view_not_admin(self):
        self.client.login(username='user', password='nachocheese')
        response = self.client.get('/addscore/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/addscore/1')

    def test_view_url_accessible_by_name(self):
        self.client.login(username='admin', password='nachocheese')
        response = self.client.get(reverse('addscore', kwargs={'gameid': 1}))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        self.client.login(username='admin', password='nachocheese')
        response = self.client.get(reverse('addscore', kwargs={'gameid': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_score.html')
    
    def test_view_has_form(self):
        login = self.client.login(username='admin', password='nachocheese')
        response = self.client.get('/addscore/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['form'], AddScoreForm)
    
    def test_view_has_gameid(self):
        login = self.client.login(username='admin', password='nachocheese')
        response = self.client.get('/addscore/1')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.context['gameid'], int)


class DeleteScoreViewTest(TestCase):
    def setUp(self):
        # Create users
        User.objects.create_user(username='user', password = 'nachocheese')
        User.objects.create_superuser(username='admin', password = 'nachocheese')
        # Create teams
        team1 = Team.objects.create(name='team1')
        team2 = Team.objects.create(name='team2')
        # Create game
        Game.objects.create(bowl='game1', team1=team1, team2=team2, date='2023-12-26', team1_score=7, team2_score=21)

    def test_view_url_exists_at_desired_location(self):
        login = self.client.login(username='admin', password='nachocheese')
        response = self.client.get('/deletescore/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/setup')
    
    def test_view_logged_out(self):
        response = self.client.get('/deletescore/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/deletescore/1')
    
    def test_view_user_is_not_admin(self):
        login = self.client.login(username='user', password='nachocheese')
        response = self.client.get('/deletescore/1')
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/accounts/login/?next=/deletescore/1')

    def test_view_url_accessible_by_name(self):
        login = self.client.login(username='admin', password='nachocheese')
        response = self.client.get(reverse('delete_score', kwargs={'gameid': 1}))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, '/setup')