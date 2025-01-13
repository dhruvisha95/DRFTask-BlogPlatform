from rest_framework import serializers
from .models import Blog, Comments, Tag, Category
from users.serializers import CustomUserSerialzer
from users.models import CustomUser


class TagSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Tag
        fields = ['tag']


class CategorySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Category
        fields = ['category']

class CommentSerializer(serializers.ModelSerializer):

    author = CustomUserSerialzer()

    class Meta:
        model = Comments
        fields = ['comment']

class BlogPostSerializer(serializers.ModelSerializer):
    tags = TagSerializer(many=True)
     
    class Meta:
        model = Blog
        fields = ['title', 'publication_date', 'blog_content', 'category', 'tags', 'author']

    def create(self, validated_data):
        tags_data = validated_data.pop('tags', [])
        blog = Blog.objects.create(**validated_data)

        tags = []
        for tag_data in tags_data:
            tag, _ = Tag.objects.get_or_create(tag=tag_data['tag'])
            tags.append(tag)
        blog.tags.set(tags)

        return blog
    
class BlogSerializer(serializers.ModelSerializer):

    tags = TagSerializer(many = True)
    category = CategorySerializer()
    comments = CommentSerializer(many = True)

    class Meta:
        model = Blog
        fields = ['title', 'publication_date', 'blog_content', 'category', 'tags', 'comments']


