from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User

class BetUser(models.Model):
	user = models.OneToOneField(User)

	# Extend User model to include Venmo Authorization Information
	venmoid = models.CharField(unique=True)
	venmoname = models.CharField(unique=True)
	access_token = models.CharField()
	refresh_token = models.CharField()

	def getfriends(self):
		return Friendship.objects.filter(Q(to_user=self)|Q(from_user=self))

	class Meta:
		return self.user.username


class Bet(models.Model):
	bet = models.CharField(max_length=140)
	bettor = models.ForeignKey(User)
	bettee = models.ForeignKey(User)
	won = models.BooleanField(default=False)
	paid = models.BooleanField(default=False)
	winner = models.ForeignKey(User)

	def __unicode__(self):
		return self.bet[:10]

class Friendship(models.Model):    
    to_user = models.ForeignKey(BetUser, related_name="friends")
    from_user = models.ForeignKey(BetUser, related_name="_unused_")
    
    class Meta:
        unique_together = (('to_user', 'from_user'),)