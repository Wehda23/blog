"""
File Contains Serialization Classes:

    - PostSerializer (serializer.ModelSerializer): Class to serialize model posts
    - PostCreateSerializer (serializer.Serializer): Class used to act serializer form for creating Post.
    - PostModificationSerializer (serializer.Serializer): Class acts as a serializer form to update or delete post.
    - PostListSerializer (serializer.Serializer): Class acts as a serializer form Validator.
"""
from rest_framework import serializers
from user_authentication.serializer import UserSerializer
from .models import Post
from user_authentication.models import User
from typing import Self


# Create a Model serializers
class PostSerializer(serializers.ModelSerializer):
    author = UserSerializer()
    class Meta:
        model = Post
        fields: str = "__all__"


# Create Form Serializers.
class PostCreateSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=200)
    content = serializers.CharField()
    
    def validate_title(self: Self, value: str) -> str:
        """
        Validation Method used to validate the title of the post
        """
        # Check if title is an empty title
        if not value:
            raise serializers.ValidationError("Can't create post with an empty title!.")
        # Check if title contains only digits
        if value.isdigit():
            raise serializers.ValidationError("Post title should also contain characters!.")
        # Return Title
        return value

    def validate_content(self: Self, value: str) -> str:
        """
        Validation Method used to validate content of a post.
        """
        # Check if content is empty
        if not value:
            raise serializers.ValidationError("Can't create post with empty content!.")
        # Return Content
        return value
    
    def validate(self: Self, attr: dict) ->dict:
        """
        Method used to validate data
        """
        # Get the request user
        author = self.context.get("author")
        # Check if user is not None
        if author is None:
            raise serializers.ValidationError("Author must be provided in serializer context.")
        # Add Author to validated Data
        return attr

    def create(self: Self, validated_data: dict) -> Post:
        """
        Method used to create a new post object and relate it to the request.user

        Args:
            - validated_data (dict): Is an object that holds the validated data.

        Returns:
            - Newly created post instance.
        """
        # Get the request user
        user: User = self.context.get("author")
        # Create new post
        post: Post = Post.objects.create(**validated_data, author=user)
        # Return Post
        return post

class PostModificationSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(max_length=200, required=True)
    content = serializers.CharField(required=True)
    author = serializers.DictField(read_only=True, required=True)

    # We will add another layer of protection incase if some one remove IsAuthor Permission in permission_classess
    def validate_id(self: Self, value: str) -> str:
        """Method to validate existance of post by id"""
        # Write your logic
        return value

    def validate_author(self, value: dict) -> dict:
        """Method to validate the author of the post"""
        # Write your logic
        return value

    def valiadate_title(self: Self, value: str) -> str:
        """Validate the title of the post"""
        # Write your logic
        return value
    
    def validate_content(self: Self, value: str) -> str:
        """Validate the content of the post"""
        # Write your logic
        return value
    
    def validate(self: Self, attr: dict) -> dict:
        """Validate data"""
        # Here we need to validate the relation between the author and the post
        # Write your logic
        return attr

    def update(self: Self, instance: Post,  validated_data: dict) -> Post:
        pass


