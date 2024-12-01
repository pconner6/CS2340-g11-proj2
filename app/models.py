from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    spotify_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)

    @classmethod
    def get_or_create_by_spotify_id(cls, spotify_id, email=None):

        user, created = cls.objects.get_or_create(spotify_id=spotify_id, defaults={'email': email})
        return user, created



class Wrapped(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wrapped_items")
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
