from django.shortcuts import render
from django.contrib.auth.models import User
from django.db.models import Q
from bets.models import Bet
from rest_framework import viewsets
from bets.serializers import UserSerializer, BetSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def bets(self, request, *args, **kwargs):
        return Bet.filter(Q(bettor=self)|Q(bettee=self))

class BetViewSet(viewsets.ModelViewSet):
    queryset = Bet.objects.all()
    serializer_class = BetSerializer