from django.contrib import admin
from .models import Player, Team, Transfer


@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):
    list_display = ("name", "position", "value")
    search_fields = ("name",)
    list_filter = ("position",)


@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ("user", "capital")
    search_fields = ("user__username",)
    list_filter = ("capital",)


@admin.register(Transfer)
class TransferAdmin(admin.ModelAdmin):
    list_display = ("player", "seller", "buyer", "price", "is_active")
    search_fields = ("player__name", "seller__user__username", "buyer__user__username")
    list_filter = ("is_active",)
