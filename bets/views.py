from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.decorators import action, link
from bets.models import Bet, BetUser
from dollarbets.settings import CLIENT_ID, CLIENT_SECRET
from rest_framework import viewsets, generics
from rest_framework.response import Response
from bets.serializers import UserSerializer, BetSerializer
import requests

"""
To-Dos:
Friends view so that friends can be updated through a Venmo user/:userid/friends API call every so often. When a user first signs up the view should check through all venmo friends and see if any are users on dollar bets, if they are then create a friendship.
    Consider: What happens when two people are already on dollar bets and they become friends on Venmo.
    Options: 
        Ignore it and only create friendships when new users join (similar to venmo sending notifications when a facebook friend joins.)
        Every n-th visit or n-days check for new venmo friends in order to avoid constant costly operations like checking all of a users friends every time they log in.
Charge View? or just include that in data during a POST to the pay view so the value can be -1.0 instead.
    Other Option: ignore charges and if a user claims to have won a bet then include that bet in the losers notifications
    Problems: User Honesty (my friends usually pay up for dollar bets, but would other users? Maybe include a mission statement like "we honor bets" or something for new users to see?)
"""

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Read-Only ViewSet for Users because all Users are created through Venmo OAuth.  Allow filtering through venmousername in order to get specific users.

    To-Do: Possibly add more filter-fields depending on how profiles will work.
    """
    queryset = BetUser.objects.all()
    serializer_class = UserSerializer
    filter_fields = ('venmoname',)


class BetViewSet(viewsets.ModelViewSet):
    """
    Default rest_framework ModelViewSet in order to list and create bets.
    """

    queryset = Bet.objects.all()
    serializer_class = BetSerializer

def venmoauth(request):
    """
    This is the view that Venmo redirects to from their authorization page.  Venmo returns a authorization code which can be used with the API keys to get access and refresh tokens for the user.
    """

    # Get auth code returned by Venmo
    AUTH_CODE = request.GET.get('code')
    data = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": AUTH_CODE}
    url = "https://api.venmo.com/v1/oauth/access_token"

    # POST data to Venmo's oauth to get access and refresh tokens
    response = requests.post(url, data)
    response_dict = response.json()
    access_token = response_dict.get('access_token')
    refresh_token = response_dict.get('refresh_token')
    
    # Put returned user info into dict to look up or create User/BetUser
    vuser = response_dict.get('user')
    username = vuser['username']
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User()
        user.username = username
        user.password = access_token
        user.email = vuser['email']
        user.first_name = vuser['first_name']
        user.last_name = vuser['last_name']
        user.save()
    try:
        betuser = BetUser.objects.get(user=user)
    except BetUser.DoesNotExist:
        betuser = BetUser()
        betuser.user = user
        betuser.venmoid = vuser['id']
        betuser.venmoname = username
        betuser.access_token = access_token
        betuser.refresh_token = refresh_token
        betuser.save()

    # Force login in order to avoid handling passwords
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)

    # Redirect Logged in User
    return HttpResponseRedirect('/api/v1/')

def pay(request):
    """
    Simple payment POST to the Venmo API.  The POST JSON should include the access_token of the paying user, the user_id of the receiving user, and the bet string.
    """

    url = 'https://api.venmo.com/v1/payments'
    access_token = request.GET.get('access_token')
    user_id = request.GET.get('user_id')
    bet = request.GET.get('bet')
    data = {
        'access_token': access_token,
        'user_id': user_id,
        'note': bet,
        'amount': 1.0
    }
    response = requests.post(url,data)
    return HttpResponseRedirect('/api/v1/')
