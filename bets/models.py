from django.db import models
from django.contrib.auth.models import User

class BetUser(models.Model):
    """
    Extension of default Django User model to add given access and refresh token as well as venmo user info.

    Things to think about:
    venmoname isn't necessary if user.username is set to venmoname and the user can't update info. (doesn't really matter what the username is if everything is done with venmoid and access_token)
    will probably have to add venmo photo url, but not a priority
    """

    user = models.OneToOneField(User)

    # Extend User model to include Venmo Authorization Information
    venmoid = models.CharField(max_length=200,unique=True)
    venmoname = models.CharField(max_length=200,unique=True)
    access_token = models.CharField(max_length=200,)
    refresh_token = models.CharField(max_length=200,)

    def getfriends(self):
        friends = []
        for friendship in Friendship.objects.filter(from_user=self):
            friends.append(friendship.to_user)
        for friendship in Friendship.objects.filter(to_user=self):
            friends.append(friendship.from_user)
        return friends

    def __unicode__(self):
        return self.user.username

class Bet(models.Model):
    """
    Model for users to make bets.
    bettor: bet initiator
    bettee: bet recipient
    agreed: boolean for whether bettee has accepted the bet (most likely through some view similar to venmo's charge notification view)
    """

    bet = models.CharField(max_length=140)
    bettor = models.ForeignKey(BetUser, related_name="made")
    bettee = models.ForeignKey(BetUser, related_name="accepted")
    agreed = models.BooleanField(default=False)
    won = models.BooleanField(default=False)
    paid = models.BooleanField(default=False)
    winner = models.ForeignKey(User, null=True)

    def __unicode__(self):
        return self.bet

class Friendship(models.Model):
    """
    Model to for friendships between users.  Friendship will only be created when a user authorizes with Venmo.
    """

    to_user = models.ForeignKey(BetUser, related_name="friends")
    from_user = models.ForeignKey(BetUser, related_name="_unused_")
    
    class Meta:
        unique_together = (('to_user', 'from_user'),)

    def __unicode__(self):
        return self.to_user.user.username + "|" + self.from_user.user.username