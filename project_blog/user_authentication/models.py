"""
File that contains Model classes for the API:-
    - User (AbstractUser): Custom made Authentication User class.
"""
from django.contrib.auth.models import AbstractUser


# Create Authentication User Model
class User(AbstractUser):
    pass

