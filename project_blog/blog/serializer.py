"""
File Contains Serialization Classes:

    - PostSerializer (serializer.ModelSerializer): Class to serialize model posts
    - ListAuthorPostsSerializer (serializer.ModelSerializer): Class used to list all posts for an author.
    - PostModificationSerializer (serializer.Serializer): Class acts as a serializer form validator.
    - PostListSerializer (serializer.Serializer): Class acts as a serializer form Validator.
"""
from rest_framework import serializers
from user_authentication.models import User
from .models import Post
from typing import Self


# Create a Model serializers
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields: str = "__all__"

class ListAutherPostsSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True)
    class Meta:
        model = User
        fields: tuple[str] = (
            "username",
            "first_name",
            "last_name",
            "posts"
        )
    

# Create Form Serializers.
class PostModificationSerializer(serializers.Serializer):
    
    def validate(self, attrs: dict) -> dict:
        pass

    def create(self, validated_data: dict) -> Post:
        pass

    def update(self, instance: Post, validated_data: dict) -> Post:
        pass

class PostListSerializer(serializers.Serializer):
    pass

