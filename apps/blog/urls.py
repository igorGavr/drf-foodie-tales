from django.urls import path
from .views import (PostListAPIView, CategoryListAPIView, PostRetrieveUpdateDestroyView,
                    CategoryRetrieveUpdateDestroyView,

                    )

urlpatterns = [
    path('posts/', PostListAPIView.as_view()),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('categories/', CategoryListAPIView.as_view()),
    path('categories/<int:pk>/', CategoryRetrieveUpdateDestroyView.as_view()),

]
