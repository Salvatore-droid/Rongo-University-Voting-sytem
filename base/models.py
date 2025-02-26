from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Voter(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    email = models.EmailField(null=True, max_length=200)
    
    
    def __str__(self):
        return self.email, self.user

class Position(models.Model):
    position = models.CharField(max_length=200, null=True)

class Candidate(models.Model):
    name = models.CharField(max_length=200, null=True)
    image = models.ImageField(null=True, blank=True)
    bio = models.TextField(null=True)

    def __str__(self):
        return self.name

    @property

    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url


    
    