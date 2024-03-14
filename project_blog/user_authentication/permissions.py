"""
File that contains General Permission CLasses:-
    - IsActiveUser (BasePermission): Is a class that validates if a user is active or not.
"""
from rest_framework.permissions import BasePermission
from django.contrib.auth.models import AnonymousUser
from typing import Self
from .models import User


class IsActiveUser(BasePermission):
    """
    Class to check if a user is active or not
    """
    def validate_user(self: Self, email: str) -> bool:
        """
        Method to get the user by his email

        Args:
            - email (str): Email of the user.
        
        Returns:
            - False in case the user does not exists or \
                returns user active status which can either be True or False.
        """
        # Check if user exists
        if not User.objects.filter(email=email).exists():
            return False
        # Grab User
        user: User = User.objects.get(email=email)
        # Return user's active status.
        return user.is_active

    def has_permission(self: Self, request: object, view) -> bool:
        """Method to check user"""
        if isinstance(request.user, AnonymousUser):
            # Check if key email exists, if not just return False.
            if not "email" in request.data:
                return False
            # Check user is active or not
            return self.validate_user(request.data["email"])
        # Return user's active status.
        return request.user.is_active
