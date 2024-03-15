"""
File that contains Permission classess for this API:-
    - IsAuthor (BasePermission) - Is a Permission Class to check if request sender is author of the post\
                If the sender is not the actual author of the post Unallowed
                If the post does not exist with this ID unallowed.
"""
from rest_framework.permissions import BasePermission
from typing import Self
from .models import Post

class IsAuthor(BasePermission):
    def has_permission(self: Self, request: object, view) -> bool:
        """Method to check user"""
        # Get post id
        pk: str = view.kwargs.get("pk")
        # incase ID is none
        if pk is None:
            return False
        # Get the post
        post: Post = Post.objects.filter(id=pk).first()
        # No post
        if post is None:
            return False
        # Check if the requesting user is author of the post
        return request.user == post.author