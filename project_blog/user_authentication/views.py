from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from .permissions import IsActiveUser
from rest_framework.permissions import BasePermission
from typing import Self


class LoginView(APIView):
    """
    This view will be used for the purpose of a user to Login/Reset Password.
    
    Attributes:
        - permission_classes (tuple): Variable that contains all permission classes for this LoginView API.
    """
    # Add class attribute  which specifies that this view is only accessible if the user is an active user or not.
    permission_classes: tuple[BasePermission] = (IsActiveUser,)

    def post(self: Self, request: object, *args, **kwargs) -> Response:
        """
        Post API view that is concerned with user login to obtain a new Token in case of success.

        Args:
            - request (object): Data obtain from the post request.
        
        Returns:
            - Incase user creditentials are valid will Return a response with user data and a new token\
                other wise will return an error code 404 not found as indication of user credientials failure.
        """
        return Response("Waheed");