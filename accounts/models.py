from collections.abc import Iterable
from django.db import models
from django.conf import settings
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
User = settings.AUTH_USER_MODEL


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    TIER_CHOICES = (
        ("Basic", "Basic"),
        ("Premium", "Premium"),
        ("Enterprise", "Enterprise"),
        ("Custom", "Custom"),
    )

    TIER_DEFAULTS = {
        "Basic": {
            "height_1": 200,
            "height_2": 0,
            "original_link": False,
            "generate_link": False,
        },
        "Premium": {
            "height_1": 200,
            "height_2": 400,
            "original_link": True,
            "generate_link": False,
        },
        "Enterprise": {
            "height_1": 200,
            "height_2": 400,
            "original_link": True,
            "generate_link": True,
        },
    }

    tier = models.CharField(max_length=15, choices=TIER_CHOICES, default="Basic")
    height_1 = models.PositiveIntegerField(
        default=200, verbose_name="Thumbnail #1 height"
    )
    height_2 = models.PositiveIntegerField(
        default=0, verbose_name="Thumbnail #2 height"
    )
    original_link = models.BooleanField(default=False)
    generate_link = models.BooleanField(
        default=False, verbose_name="Can generate links"
    )

    def __str__(self):
        return f"{self.user.username} (Tier:{self.tier})"

    def save(self, *args, **kwargs):
        if self.tier != "Custom":
            for key, value in self.TIER_DEFAULTS[self.tier].items():
                setattr(self, key, value)
        super().save(*args, **kwargs)


@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        user_profile = Profile(user=instance)
        user_profile.save()
