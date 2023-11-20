from django.db import models
from django.contrib.auth.models import User
from django.db.models import Q

class Team(models.Model):
    """Model representing a team. Just a name for now"""
    name = models.CharField(max_length=30)
    # TODO add constraint on name being unique

    def __str__(self):
        return self.name

class Game(models.Model):
    bowl = models.CharField(max_length=30)
    team1 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team1")
    team2 = models.ForeignKey(Team, on_delete=models.CASCADE, related_name="team2")
    date = models.DateField()
    team1_score = models.PositiveBigIntegerField("Team 1 Score", null=True)
    team2_score = models.PositiveBigIntegerField("Team 2 Score", null=True)

    def __str__(self):
        return f'{self.bowl}: {self.team1} vs {self.team2} @ {self.date}'

class Participant(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    is_self = models.BooleanField()
    # TODO Add constraint on name to be unique

    def __str__(self):
        return f'User: {self.user} has participant: {self.name}'
    
    class Meta:
        order_with_respect_to = "user"

class Pick(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    winner = models.ForeignKey(Team, on_delete=models.CASCADE, null=True)
    winby = models.PositiveIntegerField(null=True)
    lastChange = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(Participant, on_delete=models.CASCADE)
    # TODO Add contraint so game and owner is unique

    def get_loser(self):
        """Get the loser's team name for the Pick object."""
        if self.winner == None:
            return None
        return self.game.team2 if (self.game.team1 == self.winner) else self.game.team1
    
    # def get_winner_options(self):
    #     return (self.game.team1, self.game.team2)

    def __str__(self):
        loser = self.get_loser()
        if self.winner == None or self.winby == None:
            return f'{self.id} {self.game.bowl}: {self.owner.name} has not made a pick yet.'
        else:
            return f'{self.id} {self.game.bowl}: {self.owner.name} picks {self.winner.name} beats {loser.name} by {self.winby}'
    
    class Meta:
        order_with_respect_to = "owner"
    