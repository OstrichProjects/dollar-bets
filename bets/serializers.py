from django.contrib.auth.models import User
from bets.models import Bet
from rest_framework import serializers

class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('username','email','made','accepted')

class BetSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Bet
        fields = ('bet','bettor','bettee','won','paid','winner',)