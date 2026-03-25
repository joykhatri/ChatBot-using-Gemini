from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = None
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True, default='example@gmail.com')
    password = models.CharField(max_length=150)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.name

class Chat(models.Model):
    user = models.TextField()
    gemini = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user
    
