from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponse
from rest_framework.decorators import action, link
from bets.models import Bet, BetUser
from dollarbets.settings import CLIENT_ID, CLIENT_SECRET
from rest_framework import viewsets
from rest_framework.response import Response
from bets.serializers import UserSerializer, BetSerializer
import requests

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    @link()
    def friends(self, request, pk=None):
        user = User.objects.get(pk=pk)
        user = BetUser.objects.get(venmoname=user.username)
        queryset = user.getfriends()
        if len(queryset)>1:
            serializer = UserSerializer(queryset,many=True)
        else:
            serializer = UserSerializer(queryset)
        return Response(serializer.data)


class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer

def venmoauth(request):
    AUTH_CODE = request.GET.get('code')
    data = {"client_id": CLIENT_ID, "client_secret": CLIENT_SECRET, "code": AUTH_CODE}
    url = "https://api.venmo.com/v1/oauth/access_token"
    response = requests.post(url, data)
    response_dict = response.json()
    access_token = response_dict.get('access_token')
    refresh_token = response_dict.get('refresh_token')
    vuser = response_dict.get('user')
    username = vuser['username']
    try:
        user = User.objects.get(username=username)
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
    except User.DoesNotExist:
        user = User()
        user.username = username
        user.password = access_token
        user.email = vuser['email']
        user.first_name = vuser['first_name']
        user.last_name = vuser['last_name']
        user.save()
        betuser = BetUser()
        betuser.user = user
        betuser.venmoid = vuser['id']
        betuser.venmoname = username
        betuser.access_token = access_token
        betuser.refresh_token = refresh_token
        betuser.save()
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    login(request, user)
    return HttpResponseRedirect('/api/v1/')
