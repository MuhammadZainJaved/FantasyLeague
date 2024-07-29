from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth.models import User
from fantasy.models import Player, Team, Transfer


class FantasyFootballTests(APITestCase):

    def setUp(self):
        self.user1 = User.objects.create_user(username="user1", password="pass")
        self.user2 = User.objects.create_user(username="user2", password="pass")
        self.team1 = Team.objects.get(user=self.user1)
        self.team2 = Team.objects.get(user=self.user2)
        self.player1 = Player.objects.create(
            position="GK", value=1000000, name="Player 1"
        )
        self.player2 = Player.objects.create(
            position="DF", value=1000000, name="Player 2"
        )
        self.team1.players.add(self.player1)
        self.team2.players.add(self.player2)

    def test_registration(self):
        url = reverse("register")
        data = {
            "username": "newuser",
            "password": "newpassword",
            "email": "newuser@example.com",
        }
        response = self.client.post(url, data, format="json")
        print(response)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login(self):
        url = reverse("token_obtain_pair")
        data = {"username": "user1", "password": "pass"}
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_list_players_for_sale(self):
        url = reverse("list_player_for_sale")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_view_available_players(self):
    #     url = reverse("view_available_players")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(len(response.data) > 0)

    # def test_transfer_player(self):
    #     self.client.login(username="user2", password="pass")
    #     url = reverse("transfer_player")
    #     data = {"player_id": self.player1.id, "buyer_id": self.team2.id}
    #     response = self.client.post(url, data, format="json")
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)

    # def test_view_transfer_history(self):
    #     url = reverse("view_transfer_history")
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertTrue(len(response.data) > 0)
