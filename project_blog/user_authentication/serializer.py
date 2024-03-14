"""
File Contains Serialization Classes:-
    - UserSerializer (serializers.ModelSerializer) - Does not return user data with token.
    - LoginSerializer (serializers.ModelSerializer) - For login API & Gets user data with Token.
    - RegisterationSerializer (serializers.ModelSerializer) - for Registeration API.
    - LogoutSerializer (serializers.Serializer) - for user logout.

Notes:
    - Always use tuples because they are immutable for permissions and authentication and fields.
"""

from rest_framework import serializers
from .models import User
from .refresh_token import get_tokens_for_user
from .validators import (
    EmailValidator,
    NameValidator,
    PasswordValidator,
)
from typing import Self


# Create a serializer for user
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields: tuple[str] = (
            "email",
            "first_name",
            "last_name",
            "username",
        )

# Assuming user will login using their email address
# Create User Serializer for user login
class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields: tuple[str] = (
            "email",
            "password"
        )
        extra_kwargs: dict[str, dict] = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
        }

    def validate(self: Self, attr: object) -> object:
        """
        Method used to validate user instance.

        Args:
            - attr (object): Object that contains user details.
        
        Raises:
            - serializers.ValidationError: Incase the user does not exist or\
                User Email or Password is incorrect.
        
        Returns:
            - object incase user is valid.
        """
        # Check Email
        if not User.objects.filter(email=attr["email"]).exists():
            raise serializers.ValidationError("User Does not exist.")
        # Grab user
        user: User = User.objects.get(email=attr['email'])
        # Check Password
        if not user.check_password(attr['password']):
            raise serializers.ValidationError("User email or password is incorrect.")
        # Return object
        return attr

    # Using to_representation allow us to control serialization process.
    def to_representation(self: Self, instance: object) -> dict:
        """
        Method that allows us to control the serialization of user object.

        Args:
            - instance (object): User instance data.
        
        Returns:
            - Serialized data of user instance in form of python dictionary
        """
        data = super().to_representation(instance)
        # Get the email
        email: str = data.pop("email")
        # Get user object
        user: User = User.objects.get(email=email)
        # Get Serialized data
        data: dict = UserSerializer(user).data
        # add Token Field
        data["token"] = get_tokens_for_user(user)
        # Return Serialized Data
        return data

# Create User Registeration Serializer.
class RegisterationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)