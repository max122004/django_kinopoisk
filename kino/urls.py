from django.contrib import admin
from django.urls import path, include

from kino import views

urlpatterns = [
    path('', views.FilmListAPIView.as_view()),
    path('<int:pk>/', views.FilmDetailAPIView.as_view()),
    path('like/create/', views.LikeCreateAPIView.as_view()),
    path('liked/', views.LikedFilmAPIView.as_view()),
    path('comment/create/', views.CommentCreateAPIView.as_view()),
    path('comment/update/', views.CommentUpdateAPIView.as_view()),
    path('comment/delete/', views.CommentDeleteAPIView.as_view()),
    path('comments/', views.CommentListAPIView.as_view())
]