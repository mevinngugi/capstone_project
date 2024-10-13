from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    title = serializers.CharField(min_length=3, max_length=200, allow_blank=False)
    content = serializers.CharField(min_length=20, allow_blank=False)
    class Meta:
        model = Post
        # TODO Add tags once the model is ready
        fields = ['id', 'title', 'content', 'category', 'created_date', 'published_date']

    def validate(self, data):
        post_categories = ['Tutorial', 'Project', 'Deployment']
        if data['category'] not in post_categories:
            raise serializers.ValidationError(f'The category must be one of the following: \'{', '.join(post_categories)}\'')
        return data