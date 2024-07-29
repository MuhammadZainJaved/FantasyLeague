from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Player, Team, Transfer


class PlayerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Player
        fields = ["id", "name", "position", "value"]


class TeamSerializer(serializers.ModelSerializer):
    players = PlayerSerializer(many=True, read_only=True)
    total_value = serializers.DecimalField(
        max_digits=15, decimal_places=2, read_only=True
    )

    class Meta:
        model = Team
        fields = ["id", "user", "players", "capital", "total_value"]


class TransferSerializer(serializers.ModelSerializer):
    player = PlayerSerializer()
    seller = TeamSerializer()
    buyer = TeamSerializer()

    class Meta:
        model = Transfer
        fields = ["id", "player", "seller", "buyer", "price", "is_active"]


class UserSerializer(serializers.ModelSerializer):
    team = TeamSerializer(read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "team"]
