# accounts/models.py updated by Tyzer on 12/1/22

from django.contrib.auth.models import AbstractUser
from django.db import models

# the age should be required not allowing for a empty submission. 
class CustomUser(AbstractUser):
    age = models.PositiveIntegerField(null = True, blank = True)
