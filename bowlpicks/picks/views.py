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


def index(request):
    #return HttpResponse("Hello, world. You're at the picks index.")
    return render(request, 'base.html')



@login_required
def editPicks(request, userid, pickid):
    existing_pick = Pick.objects.get(id=pickid)
    if request.method == "POST":
        form = EditPicksForm(pickid, request.POST)
        if form.is_valid():
            if Participant.objects.get(id=userid).user == request.user:
                existing_pick.winner = Team.objects.get(id=form.cleaned_data["winner"][0])
                existing_pick.winby = form.cleaned_data["winby"]
                existing_pick.save()
                return HttpResponseRedirect(f"/my-picks/{userid}")
            else:
                return HttpResponse('FAILED: User doesn\'t have access to edit pick. Participant doesn\'t belong to user. <a href="/my-picks">back</a>')
    else:
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

            # Create pick for every game for the new user.
            query_games = Game.objects.all()
            for g in query_games:
                new_pick = Pick(game=g, winner=None, winby=None, owner=new_participant)
                new_pick.save()

            return HttpResponseRedirect("")
        
        if form.is_valid() and userid != None:
            # If recived a user id then we will change an existing user.
            existing_participant = Participant.objects.get(id=userid)
            existing_participant.name = form.cleaned_data["name"]
            existing_participant.save()
            return HttpResponseRedirect("")
    else:
        form = AddParticipantForm(instance=Participant.objects.get(id=userid)) if userid != None else AddParticipantForm()
    return render(request, 'account.html', {"registerForm": form, 'linkedUsers': linked_users})



def check_admin(user):
   return user.is_superuser

@user_passes_test(check_admin)
def adminPage(request):
    return render(request, 'admin_page.html')



@login_required
def groupPicks(request, layout='users', userorgame=None):
    if userorgame == None and layout == 'users':
        userorgame = Participant.objects.filter(user=request.user).get(is_self=True)
    elif userorgame == None and layout == 'games':
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
        print(games)
        print(game_query)


    # users = [(0, "Andrew"), (1, "Bracken"), (2, "William"), (3, "Jake"), (4, "Dallin"), (5,"katelyn"), (6, "Celeste")]
    # bowls = [(0,"Cotton Bowl"), (1,"Orange Bowl"), (2,"Fiesta Bowl"), (3,"Rose Bowl"), (4,"Alamo Bowl")]

    return render(request, 'group_picks.html', {
        "users": users,
        "games": games,
        "bowls": bowls,
        "picks": picks,
        "layout": layout,
        "userorgame":userorgame})



def login(request):
    return render(request, 'registration/login.html')


# Participant.objects.aggregate(id=Min("id"))['id']
@login_required
def myPicks(request, user=None):
    if user == None:
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
    GROUPCODE = 'football'

    if request.method == 'POST':
        form = RegisterUserForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['groupcode'] != GROUPCODE:
                return HttpResponse("FAILED. Incorrect groupcode. Group doesn't exist. <a href= '/register'>Back</a>")
            elif form.cleaned_data['password'] != form.cleaned_data['password']:
                return HttpResponse("FAILED. Passwords do not match. <a href= '/register'>Back</a>")
                #TODO Change this to be part of form validation.
            
            else:
                user = User.objects.create_user(form.cleaned_data['username'])
                user.set_password(form.cleaned_data['password'])
                user.save()
                new_participant = Participant(name=form.cleaned_data['username'].capitalize(), user=user, is_self=True)
                new_participant.save()

                # Create pick for every game for the new user.
                query_games = Game.objects.all()
                for g in query_games:
                    new_pick = Pick(game=g, winner=None, winby=None, owner=new_participant)
                    new_pick.save()

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
            # Create new game.
            data = form.cleaned_data
            new_game = Game(bowl=data["bowl"], team1=data["team1"], team2=data["team2"], date=data["date"])
            new_game.save()

            # Create a pick for each existing user for this game.
            query_participants = Participant.objects.all()
            for p in query_participants:
                new_pick = Pick(game=new_game, winner=None, winby=None, owner=p)
                new_pick.save()

            return HttpResponseRedirect("")
        
        if form.is_valid() and gameid != None:
            # Get and Edit existing game.
            existing_game = Game.objects.get(id=gameid)
            existing_game.bowl = form.cleaned_data["bowl"]
            existing_game.team1 = form.cleaned_data["team1"]
            existing_game.team2 = form.cleaned_data["team2"]
            existing_game.date = form.cleaned_data["date"]
            existing_game.save()

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
        if form.is_valid() and teamid == None:
            data = form.cleaned_data
            new_team = Team(name=data["name"])
            new_team.save()
            return HttpResponseRedirect("")
        if form.is_valid() and teamid != None:
            existing_team = Team.objects.get(id=teamid)
            existing_team.name = form.cleaned_data["name"]
            existing_team.save()
            return HttpResponseRedirect("")
    else:
        form = AddTeamForm(instance=Team.objects.get(id=teamid)) if teamid != None else AddTeamForm()

    return render(request, 'add_team.html', {"form": form, "teams": teams})

@user_passes_test(check_admin)
def deleteGame(request, gameid):
    game = Game.objects.get(id=gameid)
    game.delete()
    return HttpResponseRedirect("/setup")

@user_passes_test(check_admin)
def deleteTeam(request, teamid):
    team = Team.objects.get(id=teamid)
    team.delete()
    return HttpResponseRedirect("/addteam")

@login_required
def logout_view(request):
    logout(request)
    return render(request, 'registration/login.html')

@login_required
def deleteParticipant(request, userid):
    participant = Participant.objects.get(id=userid)
    if participant.user == request.user and not participant.is_self:
        participant.delete()
        return HttpResponseRedirect("/account")
    else:
        return HttpResponse("FAILED. Participant doesn't belong to current user or participant is self. <a href= '/account'>Back</a>")