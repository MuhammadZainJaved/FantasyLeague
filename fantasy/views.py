from django.contrib.auth.models import User
from rest_framework import viewsets, permissions
from rest_framework.decorators import action, permission_classes, api_view
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from rest_framework import status
from .models import Player, Team, Transfer
from .serializers import (
    PlayerSerializer,
    TeamSerializer,
    TransferSerializer,
    UserSerializer,
)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]


class PlayerViewSet(viewsets.ModelViewSet):
    queryset = Player.objects.all()
    serializer_class = PlayerSerializer
    permission_classes = [permissions.IsAuthenticated]


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]


class TransferViewSet(viewsets.ModelViewSet):
    queryset = Transfer.objects.all()
    serializer_class = TransferSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(detail=True, methods=["post"])
    def buy(self, request, pk=None):
        transfer = self.get_object()
        buyer = request.user.team

        if transfer.is_active and transfer.buyer is None:
            if buyer.capital >= transfer.price:
                transfer.buyer = buyer
                transfer.is_active = False
                transfer.save()

                transfer.seller.capital += transfer.price
                transfer.seller.players.remove(transfer.player)
                transfer.seller.save()

                buyer.capital -= transfer.price
                buyer.players.add(transfer.player)
                buyer.save()

                # Increase player value randomly
                transfer.player.value += 100000
                transfer.player.save()

                return Response(status=status.HTTP_200_OK)
            return Response(
                {"detail": "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST
            )
        return Response(
            {"detail": "Transfer is not active"}, status=status.HTTP_400_BAD_REQUEST
        )


@api_view(["POST"])
def register(request):
    username = request.data.get("username")
    password = request.data.get("password")
    email = request.data.get("email")

    if not username or not password or not email:
        return Response(
            {"error": "Username, password and email are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    if User.objects.filter(username=username).exists():
        return Response(
            {"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.create_user(username=username, password=password, email=email)
    user.save()

    refresh = RefreshToken.for_user(user)
    return Response(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=status.HTTP_201_CREATED,
    )


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def protected_view(request):
    return Response({"message": "This is a protected view"}, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def list_player_for_sale(request):
    players_for_sale = Player.objects.filter(transfer__is_active=True)
    serializer = PlayerSerializer(players_for_sale, many=True)
    return Response(serializer.data)
