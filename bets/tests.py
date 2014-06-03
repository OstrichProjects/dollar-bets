from django.test import TestCase
from bets.models import BetUser, Bet, Friendship
from bets.serializers import UserSerializer
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase
import json

class BetUserTest(TestCase):
    def test_createUser(self):
        """
        Make sure that a user can be created using a POST.
        """

        url = 'api/v1/users/'
        data = {
            'username': 'testuser1',
            'password': 'testpass1',
            'email': 'email1@test.com'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)
    
    def test_createBetUser(self):
        user1 = User.objects.create(username='testuser1',password='testpass1',email='email1@test.com')
        """
        Make sure BetUser can be created with user.
        """
        user = User.objects.get(username='testuser1')
        BetUser.objects.create(user=user,venmoid='testid1',venmoname=user.username)
        """
        Create second BetUser from User created without the API.
        """
        user2 = User.objects.create(username='testuser2',password='testpass2',email='email2@test.com')
        BetUser.objects.create(user=user2,venmoid='testid2',venmoname=user2.username)

    def test_createFriendship(self):
        """
        Make sure two BetUsers can be friends and the BetUser's getfriends method works.
        """
        friend1 = BetUser.objects.get(venmoid='testid1')
        friend2 = BetUser.objects.get(venmoid='testid2')
        friendship = Friendship.objects.create(from_user=friend1,to_user=friend2)

        self.assertEqual(friend1.getfriends()[0],friend2.user)

    def test_createBet(self):
        """
        Make sure a bet can be made between 2 users.
        """

        friend1 = 'api/v1/users/1'
        friend2 = 'api/v1/users/2'
        url = 'api/v1/bets'
        data = {
            'bet': 'Testing is the best.',
            'bettor': friend1,
            'bettee': friend2
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data, data)