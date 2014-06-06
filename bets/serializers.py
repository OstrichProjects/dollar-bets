from django.contrib.auth.models import User
from bets.models import Bet, BetUser
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """
    Default Model Serializer for Users with all made and accepted Bets as well as Friends.

    To-Do: 
    add First and Last Names for Users (when making bets Users should be able to search by first, last, and username)
    (possibly also add email and phone number, but usually friends search for each other by name)
    """
    user = serializers.RelatedField(read_only=True)
    user_id = serializers.RelatedField(read_only=True)
    made = serializers.RelatedField(read_only=True, many=True)
    accepted = serializers.RelatedField(read_only=True, many=True)
    friends = serializers.SerializerMethodField('getfriends')

    class Meta:
        model = BetUser
        fields = ('user','user_id','venmoid','made','accepted','friends')

    # Use getfriends method defined for BetUsers to get a list of friend venmonames
    def getfriends(self, obj):
        return obj.getfriends()

class BetSerializer(serializers.ModelSerializer):
    """
    ModelSerializer for Bets.

    To-Do: think about nesting url scheme for bets inside users (ie /users/1/bets/4/) 
    """
    class Meta:
        model = Bet
        fields = ('bet','bettor','bettee','won','paid','winner',)