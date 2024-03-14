"""
File that contains Model classes for the API:-

"""
from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from user_authentication.models import User

# Create your models here.
class Post(models.Model):
    id: models.UUIDField  = models.UUIDField(primary_key=True, default=None, editable=False)
    title: models.CharField = models.CharField(max_length=255)
    content: models.TextField = models.TextField(blank=False, null=False)
    author: User = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    created_at: models.DateTimeField = models.DateTimeField(auto_now_add=True)
    updated_at: models.DateTimeField = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, max_length=255, blank=True)

    def __str__(self) -> str:
        """String representation of Post instance"""
        return f"{self.title} by {self.author}"
    
    def save(self, *args, **kwargs):
        # Create A slug if does not exist or when user updates it incase if changes slug.
        self.slug = slugify(self.title)
        # update
        self.updated_at = timezone.now()
        super().save(*args, **kwargs)