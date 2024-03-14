"""
This File contains API View classes & functions:-
    LoginView (APIView): Is a class for Login/Password Reset.
    LogoutView (APIView): Is a class for Logout of an authenticated user.
    RegisterView (APIView): Is a class view for account registeration.
    RefreshTokenView (@api_view): Is an API view for  token refreshment.
"""
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsActiveUser
from .serializer import (
    LoginSerializer,
    RegisterationSerializer,
    LogoutSerializer,
)
from .refresh_token import IsRefreshToken, get_tokens_for_user
from .models import User
from rest_framework.permissions import BasePermission
from typing import Self


class LoginView(APIView):
    """
    This view will be used for the purpose of a user to Login/Reset Password.
    
    Attributes:
        - permission_classes (tuple): Variable that contains all permission classes for this LoginView API.
    """
    # Set a serializer for the API View
    serializer_class: LoginSerializer = LoginSerializer
    # Add class attribute  which specifies that this view is only accessible if the user is an active user or not.
    permission_classes: tuple[BasePermission] = (IsActiveUser,)

    def post(self: Self, request: object, *args, **kwargs) -> Response:
        """
        Post API view that is concerned with user login to obtain a new Token in case of success.

        Args:
            - request (object): Data obtain from the post request.
        
        Returns:
            - Incase user creditentials are valid will 201 created response with user data and a new token\
                other wise will return an error code 404 not found as indication of user credientials failure.
        """
        # Get User
        user_serializer: LoginSerializer = self.serializer_class(data=request.data)
        # Validate data
        if user_serializer.is_valid():
            # Return User data with authentication token.
            return Response(user_serializer.data, status=status.HTTP_201_CREATED)
        # Return Error
        return Response(user_serializer.errors, status=status.HTTP_404_NOT_FOUND);

class LogoutView(APIView):
    """Class for User Logout"""
    # Set a serializer for the API View
    serializer_class: LogoutSerializer = LogoutSerializer
    # Add class attribute  which specifies that this view is only accessible if the user is an active user or not.
    permission_classes: tuple[BasePermission] = (IsAuthenticated,)

    def post(self: Self, request: object, *args, **kwargs) -> Response:
        """
        Post method to logout user.

        Args:
            - request (object): Object that contains refresh_token to add to blacklist.
        
        Returns:
            - Response.
        """
        # Serializer
        serializer: LogoutSerializer = self.serializer_class(data=request.data)
        # Check if data is valid
        if serializer.is_valid():
            # Add token to black list
            token: str = serializer.validated_data['refresh_token']
            # Black list the token
            RefreshToken(token).blacklist()
            return Response('User has been logged out.', status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegisterView(APIView):
    """Class for Registering a new user account"""
    # Set a serializer for the API View
    serializer_class: RegisterationSerializer = RegisterationSerializer

    def post(self: Self, request: object, *args, **kwargs) -> Response:
        """
        Post method to register a new user account

        Args:
            - request (object): Object that contains details require for registering a new account.
        
        Returns:
            - Response.
        """
        # Serializer
        serializer: RegisterationSerializer = RegisterationSerializer(data=request.data)
        # Validate the data
        if serializer.is_valid():
            # Register user using .save() method that will trigger .create() if user instance does not exist.
            user: User = serializer.save()
            # Return Response User Creation was Successful
            return Response("User account was successfully created.!", status=status.HTTP_201_CREATED)
        # Incase of error
        return Response(serializer.errors, status=status.HTTP_403_FAILED)

# Refresh token API View
@api_view(["POST"])
@permission_classes([IsRefreshToken])
def refresh_token_view(request: object, *args, **kwargs) -> Response:
    """
    Function that represents a refresh token API View

    Args:
        - request (object): Object that contains refresh token data.
    
    Returns:
        - Response containing a new access & refresh token with status 202 accepted.
    """
    # get new tokens for patient
    tokens: dict[str, str] = get_tokens_for_user(request.user)
    return Response(tokens, status=status.HTTP_202_ACCEPTED)