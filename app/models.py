from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    spotify_id = models.CharField(max_length=100, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True, null=True, blank=True)
    avatar_url = models.URLField(max_length=500, null=True, blank=True)
    following = models.ManyToManyField('self', symmetrical=False, related_name='followers', blank=True)

    @classmethod
    def get_or_create_by_spotify_id(cls, spotify_id, email=None, avatar_url =None):

        user, created = cls.objects.get_or_create(spotify_id=spotify_id, defaults={'email': email, 'avatar_url': avatar_url})
        #trying to update avatar
        if not created and avatar_url and user.avatar_url != avatar_url:
            user.avatar_url = avatar_url
            user.save()
            
        return user, created



class Wrapped(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="wrapped_items")
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    public = models.BooleanField(default=True)
    likes = models.ManyToManyField(User, related_name='liked_wrappeds', blank=True)  # Track likes

    def __str__(self):
        return f"{self.user.username}'s Wrapped on {self.created_at.strftime('%Y-%m-%d')}"

    @property
    def like_count(self):
        return self.likes.count()

    
    
    
#for debugging
def __str__(self):
    return f"{self.user.username}'s Wrapped on {self.created_at.strftime('%Y-%m-%d')}"
