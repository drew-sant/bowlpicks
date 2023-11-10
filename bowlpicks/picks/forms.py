from django import forms

from picks.models import Game
from picks.models import Team
from picks.models import Participant
from picks.models import Pick

class EditPicksForm(forms.Form):
    winner = forms.ChoiceField(label="Winner", choices =[('1', 'Option 1'), ('2', 'Option 2')])
    winby = forms.IntegerField(label="Win By", max_value = 50)

    def __init__(self, pickid, *args, **kwargs):
        super(EditPicksForm, self).__init__(*args, **kwargs)
        game = Pick.objects.get(id=pickid).game
        self.fields['winner'].choices = [(game.team1.id, game.team1.name),(game.team2.id, game.team2.name)]


# class EditPicksForm(forms.ModelForm):
#     class Meta:
#         model = Pick
#         fields = ("winner","winby")


class AddGameForm(forms.ModelForm):
    class Meta:
        model = Game
        fields = ("bowl", "team1", "team2", "date")

class AddTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ("name",)

class RegisterUserForm(forms.Form):
    username = forms.CharField(max_length=30, label='Username')
    password = forms.CharField(widget=forms.PasswordInput, label='Password')
    password2 = forms.CharField(widget=forms.PasswordInput, label='Password Again')
    groupcode = forms.CharField(max_length=30, label='Group Code')

class AddParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ("name",)