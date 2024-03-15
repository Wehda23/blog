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
    id = serializers.UUIDField(required=True)
    title = serializers.CharField(max_length=200, required=True)
    content = serializers.CharField(required=True)
    author = serializers.DictField(required=True)

    # We will add another layer of protection incase if some one remove IsAuthor Permission in permission_classess
    def validate_id(self: Self, value: str) -> str:
        """Method to validate existance of post by id"""
        # Check if post exists
        if not Post.objects.filter(id= value).first():
            raise serializers.ValidationError("Post does not exist.!")
        # For detecting malicious actions
        uuid: str = self.context.get("post_id")
        if uuid != value:
            # We can black list request sender here
            # or just send this message
            raise serializers.ValidationError("Unauthorized  action detected.")
        return value

    def validate_author(self, value: dict) -> dict:
        """Method to validate the author of the post"""
        # Check value
        if not isinstance(value, dict):
            raise serializers.ValidationError("Invalid format for author field.")
        # Check if email key does not exists
        if "email" not in value:
            raise serializers.ValidationError("Email Field Is Missing from Author.")
        user: User = self.context.get("author")
        # Check if the email is same as email of the request user
        if value['email'] != user.email:
            # You can add this user to a black list for attempting such action
            # Or just return  an error message like below
            raise serializers.ValidationError("Unauthorized  action detected.")
        # Return value
        return value

    def validate_title(self: Self, value: str) -> str:
        """
        Validation Method used to validate the title of the post
        """
        # Check if title is an empty title
        if not value:
            raise serializers.ValidationError("Can't modify post with an empty title!.")
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
            raise serializers.ValidationError("Can't modify post with empty content!.")
        # Return Content
        return value
    
    def validate(self: Self, attr: dict) -> dict:
        """Validate data"""
        # Here we need to validate the relation between the author and the post
        user: User = self.context.get("author")
        # Get the author id from the validated data
        uuid: str = attr.get("id", None)
        # If there is no id in the field
        if not uuid:
            raise serializers.ValidationError("ID for post was not provided")
        # Get Post
        post: Post = Post.objects.filter(id= uuid).first()
        if not post:
            raise serializers.ValidationError("Post Does not exist")
        # Compare user of the post to that of request sender.
        if not post.author == user:
            # Unauthorized action can add user in blacklist
            raise serializers.ValidationError("Unauthorized  action detected.")
        # assign post to self.instance
        self.instance: Post = post
        return attr

    def update(self: Self, instance: Post,  validated_data: dict) -> Post:
        """Method used to update post"""
        # Update instance
        instance.title = validated_data.get("title", instance.title)
        instance.content = validated_data.get("content", instance.content)
        instance.save()
        return instance

