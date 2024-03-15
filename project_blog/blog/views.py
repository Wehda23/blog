"""
This File contains API View classes & functions:-
    - PostView (APIView): Class for creating, updating & deleting posts.
    - PostListView (APIView): Class for Listing posts of an auther.

Protected API Views:
    - PostView Protected by (IsAuthenticated, IsActiveUser) class Permissions.

Unprotected API Views:
    - PostListView
"""
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from user_authentication.permissions import IsActiveUser
from .serializer import (
    PostListSerializer,
    PostSerializer,
)
from typing import Self

# Create your views here.
class PostView(APIView):
    """Class related to Creating, Updating and Deleting a post"""
    # Serializer
    serializer_class: PostSerializer = PostSerializer
    # Permissions
    permission_classes: tuple[BasePermission] = (IsAuthenticated, IsActiveUser)

    # API Post method to create new post
    def post(self: Self, request: object, *args, **kwargs) -> Response:
        pass
    
    # API post method to update new post
    def put(self: Self, request: object, *args, **kwargs) -> Response:
        pass
    
    # API  Method to delete the existing post
    def delete(self: Self, request: object, *args, **kwargs) -> Response:
        pass

class PostsListView(APIView):
    """Class to list posts"""
    # Serializer
    serializer_class: PostListSerializer = PostListSerializer

    def get(self: Self, request: object, *args, **kwargs) -> Response:
        """Get  Method for List of all the posts"""
        pass