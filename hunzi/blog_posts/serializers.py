from rest_framework import serializers
from .models import Post, Comment


class PostSerializer(serializers.ModelSerializer):
    """Serialize, Deserialize and Validate data for the Post model."""
    title = serializers.CharField(min_length=3, max_length=200, allow_blank=False)
    content = serializers.CharField(min_length=20, allow_blank=False)
    # Mark the author field as read only 
    author = serializers.CharField(read_only=True)
    # Add number of comments a post has
    comments = serializers.SerializerMethodField()

    class Meta:
        model = Post
        # TODO Add tags once the model is ready
        fields = ['id', 'title', 'content', 'author', 'category', 'comments', 'created_date', 'published_date']

    def get_comments(self, obj):
        return Comment.objects.filter(post=obj).count()

    def validate(self, data):
        post_categories = ['Tutorial', 'Project', 'Deployment']
        if data['category'] not in post_categories:
            raise serializers.ValidationError(f'The category must be one of the following: \'{', '.join(post_categories)}\'')
        return data


class CommentSerializer(serializers.ModelSerializer):
    """Serialize, Deserialize and Validate data for the Comment model."""
    content = serializers.CharField(min_length=3, max_length=200, allow_blank=False)
    post = serializers.CharField(read_only=True)
    author = serializers.CharField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'post', 'author', 'created_at', 'updated_at']