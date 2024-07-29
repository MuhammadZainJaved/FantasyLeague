import random
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver


class Player(models.Model):
    POSITION_CHOICES = [
        ("GK", "Goalkeeper"),
        ("DF", "Defender"),
        ("MF", "Midfielder"),
        ("FW", "Forward"),
    ]

    name = models.CharField(max_length=100)
    position = models.CharField(max_length=2, choices=POSITION_CHOICES)
    value = models.DecimalField(max_digits=10, decimal_places=2, default=1000000)

    def __str__(self):
        if not self.name:
            return "dummy_" + str(random.randint(0, 10000))
        return self.name


class Team(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    players = models.ManyToManyField(Player)
    capital = models.DecimalField(max_digits=15, decimal_places=2, default=5000000)

    def total_value(self):
        return sum(player.value for player in self.players.all())

    def __str__(self):
        return f"{self.user.username}'s team"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not self.players.exists():
            # Assign 20 initial players to the new team
            positions = ["GK"] * 2 + ["DF"] * 6 + ["MF"] * 6 + ["FW"] * 6
            for position in positions:
                player = Player.objects.create(position=position, value=1000000)
                self.players.add(player)
            self.save()


class Transfer(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    seller = models.ForeignKey(
        Team, related_name="players_selling", on_delete=models.CASCADE
    )
    buyer = models.ForeignKey(
        Team,
        related_name="players_buying",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"Transfer of {self.player.name} from {self.seller.user.username}"


@receiver(post_save, sender=User)
def create_user_team(sender, instance, created, **kwargs):
    if created:
        Team.objects.get_or_create(user=instance)
