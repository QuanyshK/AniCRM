from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    is_manager = models.BooleanField(default=False) 
    is_admin = models.BooleanField(default=False) 

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


    def __str__(self):
        return f'{self.user.username} Profile'

