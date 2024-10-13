from django.db import models
from accounts.models import CustomUser

# Create your models here.
class Post(models.Model):
    title = models.CharField(max_length=200, null=False, blank=False)
    content = models.TextField(null=False, blank=False)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Consider using choices or better yet have a different model to store categories 
    category = models.CharField(max_length=50, null=False, blank=False)
    created_date = models.DateTimeField(auto_now_add=True)
    published_date = models.DateTimeField(auto_now=True)
    # Add Tags later
    # TODO Add blog tags

    def __str__(self):
        return f'{self.title} posted by {self.author} on {self.created_date}'