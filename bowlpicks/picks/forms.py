from django import forms

from django.core.exceptions import ValidationError

from picks.models import Game
from picks.models import Team
from picks.models import Participant
from picks.models import Pick

class EditPicksForm(forms.Form):
    winner = forms.ChoiceField(label="Winner", choices =[('1', 'Option 1'), ('2', 'Option 2')])
    winby = forms.IntegerField(label="Win By", max_value = 50, widget=forms.NumberInput(attrs={"size":10}))

    def __init__(self, pickid, *args, **kwargs):
        super(EditPicksForm, self).__init__(*args, **kwargs)
        game = Pick.objects.get(id=pickid).game
        self.fields['winner'].choices = [(game.team1.id, game.team1.name),(game.team2.id, game.team2.name)]

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

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password2 = cleaned_data.get("password2")
        groupcode = cleaned_data.get("groupcode")

        if password and password2:
            # Ensure that the password and password check match.
            if not password == password2:
                raise ValidationError(
                    "Password did not match the password check. Please re-enter the password and make sure that password again is the same."
                )
            if len(password) < 10:
                # Make sure that the length is at least 10 characters.
                raise ValidationError(
                    "Password needs to be at least 10 characters. No other restrictions."
                )
            
        if groupcode:
            # Ensure that the groupcode is correct
            # TODO: Move the groupcode to db and not hardcoded!
            if groupcode != 'football2023':
                raise ValidationError(
                    "Bad groupcode. Ensure that it is correct. Contact your admin if you believe there is a mistake."
                )

class AddParticipantForm(forms.ModelForm):
    class Meta:
        model = Participant
        fields = ("name",)