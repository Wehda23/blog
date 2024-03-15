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
from .models import Post
from typing import Self
import json


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
        """
        Method used to act as PUT API method to update post

        Args:
            - request (Request): Object that contain details related to API Request.
            - pk (str): is uuid of the post requested to apply modifications to.

        Returns:
            -  Response (Response): With message of Successfully updated post status code 200 OK.\
                 Or Error Message status code 400 Bad request.
                 Or error message status 403 Forbidden for unauthorized actions.
        """
        # Save context in a variable
        context: dict = {"author": request.user, "post_id": pk}
        # Serializer
        serializer: PostModificationSerializer = self.serializer_class(
            data= request.data, context= context
        )
        # Validate data
        if serializer.is_valid():
            # Update the existing post with validated data
            serializer.save()
            return Response("Post Updated successfully", status=status.HTTP_202_ACCEPTED)
        # in case of Unauthurized action
        if "Unauthorized  action detected." in json.dumps(serializer.errors):
            return Response(serializer.errors, status=status.HTTP_403_FORBIDDEN)
        # Error
        return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

    # API  Method to delete the existing post
    def delete(self: Self, request: Request, pk: str, *args, **kwargs) -> Response:
        """
        Method used to delete existing posts.
        """
        # Get the instance of the object based on primary key
        post: Post = Post.objects.filter(id=pk).first()
        # Check if post exists
        if not post:
            return Response("Post does not exist", status=status.HTTP_404_NOT_FOUND)
        # Check the post owner to the request user
        if request.user != post.author:
            # Can black list user or block
            return Response("Aunthorized action detected.", status=status.HTTP_403_FORBIDDEN)
        # Delete the object from database
        post.delete()
        return Response("Post deleted successfully", status=status.HTTP_204_NO_CONTENT)

class PostsListView(APIView):
    """Class to list posts"""
    # Serializer
    serializer_class: PostSerializer = PostSerializer

    def get(self: Self, request: Request, *args, **kwargs) -> Response:
        """Get  Method for List of all the posts"""
        pass