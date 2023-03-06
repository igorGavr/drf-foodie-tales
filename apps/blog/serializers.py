from rest_framework.serializers import Serializer, ModelSerializer
from .models import Post, Category


class PostListSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'


class CategoryListSerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'