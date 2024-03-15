"""
This File contains API View classes & functions:-
    - PostCreationView (APIView): Class API for creating posts.
    - PostModificationView (APIView): Class API updating & deleting posts.
    - PostListView (APIView): Class API for Listing posts of an auther.

Protected API Views:
    - PostView Protected by (IsAuthenticated, IsActiveUser) class Permissions.
    - PostModificationView Protected by (IsAuthenticated, IsActiveUser) class Permissions.

Unprotected API Views:
    - PostListView
"""
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.permissions import BasePermission
from user_authentication.permissions import IsActiveUser
from .serializer import (
    PostSerializer,
    PostModificationSerializer,
    PostCreateSerializer,
)
from .permissions import IsAuthor
from typing import Self


class PostCreationView(APIView):
    """Class related to Creating posts"""
    # Serializer
    serializer_class: PostCreateSerializer = PostCreateSerializer
    # Permissions
    permission_classes: tuple[BasePermission] = (IsAuthenticated, IsActiveUser)

    # API Post method to create new post
    def post(self: Self, request: Request, *args, **kwargs) -> Response:
        """
        Post API view to create new Posts

        Args:
            - request (Request): Object the contains request details needed to create new Post

        Returns:
            - Response (Response): with message of successfully created post status code 201 accepted\
                or Error Message status code 400 Bad request.
        """
        # get the user
        context: dict = {"author": request.user}
        # Serializer
        serializer: PostCreateSerializer = self.serializer_class(
            data=request.data,
            context=context
        )
        # Validate data
        if serializer.is_valid():
            # Create  a new Post using validated Data
            serializer.save()
            return Response("Post has been successfully created", status=status.HTTP_201_CREATED)
        # Otherwise return error
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
# Create your views here.
class PostModificationView(APIView):
    """Class related to Creating, Updating and Deleting a post"""
    # Serializer
    serializer_class: PostModificationSerializer = PostModificationSerializer
    # Permissions
    permission_classes: tuple[BasePermission] = (IsAuthenticated, IsActiveUser, IsAuthor)

    # API post method to update new post
    def put(self: Self, request: Request, pk: str, *args, **kwargs) -> Response:
        pass
    
    # API  Method to delete the existing post
    def delete(self: Self, request: Request, pk:str, *args, **kwargs) -> Response:
        pass

class PostsListView(APIView):
    """Class to list posts"""
    # Serializer
    serializer_class: PostSerializer = PostSerializer

    def get(self: Self, request: Request, *args, **kwargs) -> Response:
        """Get  Method for List of all the posts"""
        pass