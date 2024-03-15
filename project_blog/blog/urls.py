from django.urls import path
from .views import (
    PostCreationView,
    PostModificationView,
    PostsListView,
)

urlpatterns = [
    # View to list all posts.
    path("", PostsListView.as_view(), name="list-posts"),
    # View to create a post.
    path("create", PostCreationView.as_view(), name="create-post-view"),
    # View to Update or delete an existing post.
    path("<pk:str>", PostModificationView.as_view(), name="update-delete-post"),
]