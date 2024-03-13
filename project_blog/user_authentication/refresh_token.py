from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import BasePermission
from .models import User
from typing import Self

# Create token Function
def get_tokens_for_user(user: User) -> dict[str, str]:
    """
    Function used to create JWT token for the User

    Args:
        - user (User): User object to create JWT for.
    
    Returns:
        - Dictionary that contains both Access & Refresh Tokens.
    """
    refresh = RefreshToken.for_user(user)

    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }

class IsRefreshToken(BasePermission):
    """
    Class to Validate Refresh Token.
    It will check if the request has a valid refresh token\
        To be well informed as well that the class assigns user to the request
        incase the user is valid and the refresh token is valid.
    """
    def is_valid_user(self: Self, data: dict) -> bool:
        """Method used to check user validation"""
        # Check if user_id key exists within the decoded token
        if not ("user_id" in data):
            return False
        # Check if the user already exists in our user database.
        if not User.objects.filter(id=data["user_id"]).exists():
            return False
        # pass tests
        return True

    def is_refresh_token_valid(self: Self, refresh_token: str) -> bool:
        """Method used to check the token validation"""
        try:
            decoded_token = RefreshToken(refresh_token)
            return decoded_token
        except Exception as e:
            return False

    def has_permission(self, request, view) -> bool:
        """Method used to check refresh token"""
        # Grab the data
        data: dict = request.data
        # Check if "Refresh" Key exists within data or not.
        if "refresh" not in data:
            return False
        # Grab The Refresh Token
        refresh_token: str = request.data["refresh"]
        # Validate Refresh Token
        decoded_token = self.is_refresh_token_valid(refresh_token)
        # If Token was None just return False
        if not decoded_token:
            return False
        # Validate user.
        if not self.is_valid_user(decoded_token):
            return False
        # Grab the user
        user: User = User.objects.get(id=decoded_token["user_id"])
        # Assign Request.user to the User
        request.user = user
        return True
