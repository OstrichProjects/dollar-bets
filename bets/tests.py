from django.test import TestCase
from bets.models import BetUser, Bet, Friendship
from bets.serializers import UserSerializer
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

def createUsers():
    """
    Make sure BetUser can be created.
    """
    user = User.objects.create(username="testuser1",email="test1@test.com")
    betuser = BetUser.objects.create(user=user,venmoid='testid1',venmoname=user.username) # Again, it doesn't seem like venmoname is necessary
    """
    Create second BetUser from User created without the API.
    """
    user2 = User.objects.create(username='testuser2',email='test2@test.com')
    betuser2 = BetUser.objects.create(user=user2,venmoid='testid2',venmoname=user2.username)

class BetUserTest(APITestCase):
    def test_createBetUser(self):
        createUsers()
    def test_createFriendship(self):
        createUsers()
        """
        Make sure two BetUsers can be friends and the BetUser's getfriends method works.

        ***Should be done with Friends view when that gets done!
        """
        friend1 = BetUser.objects.get(venmoid='testid1')
        friend2 = BetUser.objects.get(venmoid='testid2')
        friendship = Friendship.objects.create(from_user=friend1,to_user=friend2)

        self.assertEqual(friend1.getfriends()[0],friend2)

    def test_createBet(self):
        """
        Make sure a bet can be made between 2 users.
        """
        createUsers()
        friend1 = self.client.get('/api/v1/users/1/')
        friend2 = self.client.get('/api/v1/users/2/')
        url = '/api/v1/bets/'
        data = {
            'bet': 'Testing is the best.',
            'bettor': friend1.data['user_id'],
            'bettee': friend2.data['user_id']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        for key, value in data.iteritems():
            self.assertEqual(response.data[key], value)