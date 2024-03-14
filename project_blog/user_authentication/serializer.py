"""
File Contains Serialization Classes:-
    - UserSerializer (serializers.ModelSerializer) - Does not return user data with token.
    - LoginSerializer (serializers.ModelSerializer) - For login API & Gets user data with Token.
    - RegisterationSerializer (serializers.Serializer) - for Registeration API.
    - LogoutSerializer (serializers.Serializer) - for user logout.

Notes:
    - Always use tuples because they are immutable for permissions and authentication and fields.
    - We will Use ModelSerializer for Model Based Serializers that gets a Django Models Data\
        Use Serializer for Form Based data and returns Non Django Model Data.

    Practicall a serializer takes a class and returns the __dict__ of the class.
"""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError
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
            raise serializers.ValidationError("User 'email' or 'password' is incorrect.")
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
        fields = ("first_name", "last_name", "email", "password", "username")
        extra_kwargs: dict = {
            "password": {"write_only": True, "required": True},
            "email": {"required": True},
            "first_name": {"required": True},
            "last_name": {"required": True},
            "username": {"required": True},
        }
    # Validators.
    def validate_first_name(self: Self, value: str) -> str:
        """Method to Validate first name"""
        # validate first name
        NameValidator(value, serializers.ValidationError).validate()
        return value

    def validate_last_name(self: Self, value: str) -> str:
        """Method to Validate last name"""
        # validate last name
        NameValidator(value, serializers.ValidationError).validate()
        return value

    def validate_email(self: Self, value: str) -> str:
        """
        Method validates email format
        """
        # Validate Email
        EmailValidator(value, serializers.ValidationError).validate()
        return value

    def validate_password(self: Self, value: str) -> str:
        """Method Validates Password"""
        # Validate password
        PasswordValidator(value, serializers.ValidationError).validate()
        return value

    def validate(self: Self, attrs: dict) -> dict:
        """Method used to validate registeration of a new patient account"""
        # Need to check if there is not another user already with same email
        if User.objects.filter(email=attrs["email"]).exists():
            # Raise account already exists
            raise serializers.ValidationError(
                "Patient account with this email already exists"
            )
        return attrs

    # Create new instance.
    # Use .create() method for post request, Triggers if an object does not exist.
    def create(self: Self, validated_data: dict, *args, **kwargs) -> User:
        """
        Method used to create a new User Instance/account

        Args:
            - validated_data (dict): Dictionary that contains validated data required to create new user.
        
        Returns:
            - New created user as a User Model Instance.
        """
        # Using create_user method will actually handle the password hashing for us.
        user = User.objects.create_user(**validated_data)
        # Add a functionality that creates a unique user name to avoid errors
        user.save()
        # Return User Object
        return user

class LogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField(required=True)

    # Validate token
    def validate_refresh_token(self: Self, token: str) -> str:
        """Validate JWT Token"""
        try: 
            RefreshToken(token)
            return token
        except TokenError as e:
            # Other wise raise Token validation error for token.
            raise serializers.ValidationError(e)
        except Exception as e:
            # Other wise raise ValidationError for token.
            # Log the error to the system for a follow up to the situation using a logger.
            # logger.error(f"An unexpected error occurred while trying to authenticate Refresh Token: {e}")
            raise serializers.ValidationError("Unexpected Error had occured.")
        
        