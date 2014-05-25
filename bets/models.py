from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class BetUser(models.Model):
    user = models.OneToOneField(User)

    # Extend User model to include Venmo Authorization Information
    venmoid = models.CharField(max_length=200,unique=True)
    venmoname = models.CharField(max_length=200,unique=True)
    access_token = models.CharField(max_length=200,)
    refresh_token = models.CharField(max_length=200,)

    def getfriends(self):
        friends = []
        for friendship in Friendship.objects.filter(from_user=self):
            friends.append(friendship.to_user.user)
        for friendship in Friendship.objects.filter(to_user=self):
            friends.append(friendship.from_user.user)
        return friends

    def __unicode__(self):
        return self.user.username

class Bet(models.Model):
    bet = models.CharField(max_length=140)
    bettor = models.ForeignKey(User, related_name="made")
    bettee = models.ForeignKey(User, related_name="accepted")
    won = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    winner = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.bet[:10]

class Friendship(models.Model):    
    to_user = models.ForeignKey(BetUser, related_name="friends")
    from_user = models.ForeignKey(BetUser, related_name="_unused_")
    
    class Meta:
        unique_together = (('to_user', 'from_user'),)

    def __unicode__(self):
        return self.to_user.user.username + "|" + self.from_user.user.username