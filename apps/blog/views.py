from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import (
    ListAPIView, RetrieveUpdateDestroyAPIView, GenericAPIView,
    ListCreateAPIView,

)
from rest_framework.mixins import CreateModelMixin
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny

from .models import Category, Post
from .serializers import PostListSerializer, CategoryListSerializer


class PostListAPIView(ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer
    # permission_classes = (IsAuthenticated,)

    def get_permissions(self):
        if self.request.method == 'GET':
            return AllowAny(),
        return IsAuthenticated(),

    def get_queryset(self):
        query = self.request.query_params.dict()
        queryset = super().get_queryset()
        category_slug = query.get('category_slug')

        if category_slug:
            queryset = Post.objects.filter(is_draft=False, category__slug=category_slug)
            return queryset

        # author = query.get('author')
        # print(self.request.user)
        # if author:
        #     queryset = Post.objects.filter(author=self.request.user)
        #     return queryset

        return queryset


class PostRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListSerializer


class CategoryListAPIView(ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
    # permission_classes = (IsAdminUser, )

    def get_permissions(self):
        if self.request.method == 'GET':
            return AllowAny(),
        return IsAuthenticated(),


class CategoryRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategoryListSerializer
