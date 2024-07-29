from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from .models import Player, Team, Transfer
from rest_framework_simplejwt.tokens import RefreshToken


class FantasyFootballTests(APITestCase):
    def setUp(self):
        # Create test users
        self.user1 = User.objects.create_user(
            username="user1", password="password123", email="user1@example.com"
        )
        self.user2 = User.objects.create_user(
            username="user2", password="password123", email="user2@example.com"
        )

        # Create test players
        self.player1 = Player.objects.create(name="Player 1", position="GK")
        self.player2 = Player.objects.create(name="Player 2", position="DF")

        # Create teams and assign players
        self.team1 = Team.objects.get(user=self.user1)
        self.team2 = Team.objects.get(user=self.user2)
        self.team1.players.add(self.player1)
        self.team2.players.add(self.player2)

        # Create transfers
        self.transfer = Transfer.objects.create(
            player=self.player2, seller=self.team2, price=1500000
        )

        # Generate JWT tokens
        self.refresh_token_user1 = RefreshToken.for_user(self.user1)
        self.access_token_user1 = str(self.refresh_token_user1.access_token)
        self.refresh_token_user2 = RefreshToken.for_user(self.user2)
        self.access_token_user2 = str(self.refresh_token_user2.access_token)

    def test_register(self):
        url = reverse("register")
        data = {
            "username": "user3",
            "password": "password123",
            "email": "user3@example.com",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_list_player_for_sale(self):
        url = reverse("list_player_for_sale")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data[0])
        self.assertIn("name", response.data[0])
        self.assertIn("position", response.data[0])
        self.assertIn("value", response.data[0])

    def test_user_viewset(self):
        url = reverse("user-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data[0])
        self.assertIn("username", response.data[0])
        self.assertIn("email", response.data[0])

    def test_player_viewset(self):
        url = reverse("player-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data[0])
        self.assertIn("name", response.data[0])
        self.assertIn("position", response.data[0])
        self.assertIn("value", response.data[0])

    def test_team_viewset(self):
        url = reverse("team-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data[0])
        self.assertIn("user", response.data[0])
        self.assertIn("players", response.data[0])
        self.assertIn("capital", response.data[0])
        self.assertIn("total_value", response.data[0])

    def test_transfer_viewset(self):
        url = reverse("transfer-list")
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user1)
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("id", response.data[0])
        self.assertIn("player", response.data[0])
        self.assertIn("seller", response.data[0])
        self.assertIn("buyer", response.data[0])
        self.assertIn("price", response.data[0])
        self.assertIn("is_active", response.data[0])

    def test_buy_player(self):
        url = reverse("transfer-buy", kwargs={"pk": self.transfer.id})
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + self.access_token_user1)
        response = self.client.post(url, data={"price": 1500000}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Transfer.objects.get(id=self.transfer.id).is_active)
        self.assertIn(self.player2, self.team1.players.all())
        self.assertNotIn(self.player2, self.team2.players.all())
