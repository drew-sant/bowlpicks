from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import logout
from django.contrib.auth.models import User

from picks.models import Game
from picks.models import Pick
from picks.models import Participant
from picks.models import Team

from .forms import EditPicksForm
from .forms import AddGameForm
from .forms import RegisterUserForm
from .forms import AddTeamForm
from .forms import AddParticipantForm

from django.db.models import Min

import logging
logging = logging.getLogger(__name__)


def index(request):
    #return HttpResponse("Hello, world. You're at the picks index.")
    return render(request, 'base.html')



@login_required
def editPicks(request, userid, pickid):
    existing_pick = Pick.objects.get(id=pickid)
    if request.method == "POST":
        # If we get data from request then create form with it.
        form = EditPicksForm(pickid, request.POST)
        if form.is_valid():
            if Participant.objects.get(id=userid).user == request.user:
                # Edit the pick if the participant belongs to current user.
                logging.debug(f'editPicks: Selected winner\'s id from EditPicksForm: {form.cleaned_data["winner"]}')
                existing_pick.winner = Team.objects.get(id=form.cleaned_data["winner"])
                existing_pick.winby = form.cleaned_data["winby"]
                existing_pick.save()
                logging.info(f'EDIT PICK: {request.user.username} edited pick to: {existing_pick}')
                return HttpResponseRedirect(f"/my-picks/{userid}")
            else:
                return HttpResponse('FAILED: User doesn\'t have access to edit pick. Participant doesn\'t belong to user. <a href="/my-picks">back</a>')
    else:
        # If we aren't recieving new data then fill the form with data from db.
        winner = existing_pick.winner
        winby = existing_pick.winby
        values = {"winner": winner, "winby": winby}
        form = EditPicksForm(pickid, initial=values)
    return render(request, 'edit_picks.html', {"form": form})



@login_required
def account(request, userid=None):
    query = Participant.objects.filter(user=request.user)
    linked_users = [(x.id, x.name, x.is_self) for x in query]

    if request.method == "POST":
        form = AddParticipantForm(request.POST)
        if form.is_valid() and userid==None:
            # If no userid then create new participant
            new_participant = Participant(name=form.cleaned_data["name"].capitalize(), user=request.user, is_self=False)
            new_participant.save()
            logging.info(f'PARTICIPANT CREATED: participant: "{new_participant.name}" was created by user: "{request.user.username}" is_self={new_participant.is_self}')

            # Create pick for every game for the new user.
            query_games = Game.objects.all()
            for g in query_games:
                new_pick = Pick(game=g, winner=None, winby=None, owner=new_participant)
                new_pick.save()
                logging.info(f'PICK CREATED: pick:"{str(new_pick)}" was automantically created for participant: "{new_participant.name}"')

            return HttpResponseRedirect("")
        
        if form.is_valid() and userid != None:
            # If recived a user id then we will change an existing user.
            existing_participant = Participant.objects.get(id=userid)
            old_name = existing_participant.name # for logging purposes
            existing_participant.name = form.cleaned_data["name"]
            existing_participant.save()
            logging.info(f'PARTICIPANT EDITED: participant: "{old_name}" was changed to {existing_participant.name} by user: {request.user.username}')
            return HttpResponseRedirect("")
    else:
        form = AddParticipantForm(instance=Participant.objects.get(id=userid)) if userid != None else AddParticipantForm()
    return render(request, 'account.html', {"registerForm": form, 'linkedUsers': linked_users})



def check_admin(user):
   """A test for view permission."""
   return user.is_superuser

@user_passes_test(check_admin)
def adminPage(request):
    return render(request, 'admin_page.html')



@login_required
def groupPicks(request, layout='users', userorgame=None):
    if userorgame == None and layout == 'users':
        # Default to the signedin user's participant self.
        userorgame = Participant.objects.filter(user=request.user).get(is_self=True)
    elif userorgame == None and layout == 'games':
        # Default to the minimum id in Game
        userorgame = Game.objects.aggregate(id=Min("id"))['id']
    
    user_query = Participant.objects.all()
    users = [(x.id, x.name) for x in user_query]

    game_query = Game.objects.all()
    bowls = [(x.id, x.bowl) for x in game_query]
    picks = {}
    games = {}

    if layout == "users":
        pick_query = Pick.objects.filter(owner=userorgame)
        for pick in pick_query:
            d = {}
            d['winby'] = pick.winby
            d['winner'] = pick.winner
            d['loser'] = pick.get_loser()
            picks[pick.game.bowl] = d
    else:
        game_query = Pick.objects.filter(game=userorgame)
        for pick in game_query:
            d = {}
            d['winby'] = pick.winby
            d['winner'] = pick.winner
            d['loser'] = pick.get_loser()
            games[pick.owner.name] = d

    return render(request, 'group_picks.html', {
        "users": users,
        "games": games,
        "bowls": bowls,
        "picks": picks,
        "layout": layout,
        "userorgame":userorgame})



def login(request):
    # Django's built-in login
    return render(request, 'registration/login.html')


@login_required
def myPicks(request, user=None):
    if user == None:
        # If not given a user id then we use the signed in user's participant self.
        user = Participant.objects.filter(user=request.user).get(is_self=True).id
    query = Participant.objects.filter(user=request.user)
    linked_users = [(x.id, x.name) for x in query]
    # TODO This will fail within the first try of accessing after creating the first participant for user.
    selected_user = (user, Participant.objects.get(id=user).name)
    query_picks = Pick.objects.filter(owner=Participant.objects.get(id=user))
    picks = [(x.id, x.game.bowl, f'') for x in query_picks
              if x.winner == None or x.winby == None]
    picks += [(x.id, x.game.bowl, f'{x.winner.name} beats {x.get_loser()} by {x.winby}')
             for x in query_picks
             if x.winner != None and x.winby != None]
    

    return render(request, 'my_picks.html', {"linked_users": linked_users, "selected": selected_user, "picks": picks})



def register(request):
    GROUPCODE = 'football' # TODO Move this to db and have it set/edit in setup view.

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['groupcode'] != GROUPCODE:
                # If the groupcode doesn't match then don't register user.
                return HttpResponse("FAILED. Incorrect groupcode. Group doesn't exist. <a href= '/register'>Back</a>")
            elif form.cleaned_data['password'] != form.cleaned_data['password']:
                # Make sure both password fields match each other.
                return HttpResponse("FAILED. Passwords do not match. <a href= '/register'>Back</a>")
                #TODO Change this to be part of form validation.
            else:
                # Create new user.
                user = User.objects.create_user(form.cleaned_data['username'])
                user.set_password(form.cleaned_data['password'])
                user.save()
                logging.info(f'USER CREATED: user: "{user.username}" was created.')
                # Create a new participant associated with the new user's self.
                new_participant = Participant(name=form.cleaned_data['username'].capitalize(), user=user, is_self=True)
                new_participant.save()
                logging.info(f'PARTICIPANT CREATED: Participant: "{new_participant.name}" was created automatically for "{user.username}" and is_self=True')

                # Create pick for every game for the new participant.
                query_games = Game.objects.all()
                for g in query_games:
                    new_pick = Pick(game=g, winner=None, winby=None, owner=new_participant)
                    new_pick.save()
                    logging.info(f'PICK CREATED: Pick: "{str(new_pick)}" was created automatically when participant: "{new_participant.name}" was created.')

                return HttpResponseRedirect("login")
    else:
        form =RegisterUserForm()
        return render(request, 'register.html', {'form': form})



@user_passes_test(check_admin)
def setup(request, gameid=None):
    query_game = Game.objects.all()
    # Create a list of tuples of the form (<gameid>, <text-to-display-in-list>)
    games_list = [(x.id, f'{x.bowl} - {x.team1} vs {x.team2} - {x.date}') for x in query_game]
    
    if request.method == "POST":
        form = AddGameForm(request.POST)
        if form.is_valid() and gameid == None:
            # Create new game if no gameid is provided
            data = form.cleaned_data
            new_game = Game(bowl=data["bowl"], team1=data["team1"], team2=data["team2"], date=data["date"])
            new_game.save()
            logging.info(f'GAME CREATED: game: "{str(new_game)}" was created by user: "{request.user.username}"')

            # Create a pick for each existing user for this game.
            query_participants = Participant.objects.all()
            for p in query_participants:
                new_pick = Pick(game=new_game, winner=None, winby=None, owner=p)
                new_pick.save()
                logging.info(f'PICK CREATED: pick: "{str(new_pick)}" was automatically created for game: "{new_game.bowl}"')

            return HttpResponseRedirect("")
        
        if form.is_valid() and gameid != None:
            # Get and Edit existing game if we have a gameid.
            existing_game = Game.objects.get(id=gameid)
            old_game = existing_game # Logging purposes
            existing_game.bowl = form.cleaned_data["bowl"]
            existing_game.team1 = form.cleaned_data["team1"]
            existing_game.team2 = form.cleaned_data["team2"]
            existing_game.date = form.cleaned_data["date"]
            existing_game.save()
            logging.info(f'GAME EDITED: {request.user.username} edited from "{old_game}" to {existing_game}')

            return HttpResponseRedirect("")
    else:
        form = AddGameForm(instance=Game.objects.get(id=gameid)) if gameid != None else AddGameForm()

    return render(request, 'setup.html', {"form": form, "games": games_list})

@user_passes_test(check_admin)
def addTeam(request, teamid=None):
    query_team = Team.objects.all()
    teams = [(x.id, x.name) for x in query_team]

    if request.method == "POST":
        form = AddTeamForm(request.POST)
        # If the form is valid then we process and use the data.
        if form.is_valid() and teamid == None:
            # If we don't have a team id then we create a new one.
            data = form.cleaned_data
            new_team = Team(name=data["name"])
            new_team.save()
            logging.info(f'TEAM CREATED: {request.user.username} created the new team {new_team.name}')
            return HttpResponseRedirect("")
        if form.is_valid() and teamid != None:
            # If given a team id then we edit the team name.
            existing_team = Team.objects.get(id=teamid)
            old_name = existing_team.name # logging purposes
            existing_team.name = form.cleaned_data["name"]
            existing_team.save()
            logging.info(f'TEAM EDITED: {request.user.username} edited an existing team \
                         from "{old_name}" to "{existing_team.name}"')
            return HttpResponseRedirect("")
    else:
        # If we don't get data via POST then we create our own form.
        # Populate the form with the team info if provided a team id and blank if we don't.
        form = AddTeamForm(instance=Team.objects.get(id=teamid)) if teamid != None else AddTeamForm()

    return render(request, 'add_team.html', {"form": form, "teams": teams})

@user_passes_test(check_admin)
def deleteGame(request, gameid):
    """Delete the game associated with gameid."""
    game = Game.objects.get(id=gameid)
    game.delete()
    logging.info(f'GAME DELETED: {request.user.username} deleted {game}')
    return HttpResponseRedirect("/setup")

@user_passes_test(check_admin)
def deleteTeam(request, teamid):
    """Delete the team associated with teamid."""
    team = Team.objects.get(id=teamid)
    team.delete()
    logging.info(f'TEAM DELETED: {request.user.username} deleted {team.name}')
    return HttpResponseRedirect("/addteam")

@login_required
def logout_view(request):
    """Log the user out."""
    logout(request)
    return render(request, 'registration/login.html')

@login_required
def deleteParticipant(request, userid):
    """Delete participant associated with parameter userid."""
    participant = Participant.objects.get(id=userid)
    if participant.user == request.user and not participant.is_self:
        # Only if the participant belongs to the logged in user
        # AND the participant isn't the user's own self will it be allowed deletion.
        participant.delete()
        logging.info(f'PARTICIPANT DELETED: {request.user.username} deleted {participant.name}')
        return HttpResponseRedirect("/account")
    else:
        return HttpResponse("FAILED. Participant doesn't belong to current user or participant is self. <a href= '/account'>Back</a>")

@login_required
def myParticipants(request, paricipantid):
    # TODO Migrate code from account to here for participant managment.
    pass
