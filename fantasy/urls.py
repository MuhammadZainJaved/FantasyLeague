from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .views import (
    UserViewSet,
    PlayerViewSet,
    TeamViewSet,
    TransferViewSet,
    register,
    protected_view,
    list_player_for_sale,
)

router = DefaultRouter()
router.register(r"users", UserViewSet)
router.register(r"players", PlayerViewSet)
router.register(r"teams", TeamViewSet)
router.register(r"transfers", TransferViewSet)

urlpatterns = [
    path("", include(router.urls)),
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("register/", register, name="register"),
    path("protected/", protected_view, name="protected_view"),
    path("players-for-sale/", list_player_for_sale, name="list_player_for_sale"),
]
