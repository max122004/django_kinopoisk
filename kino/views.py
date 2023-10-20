from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, CreateAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from kino.models import Film, Like, Comment
from kino.permissions import IsAuthorOrReadOnly
from kino.serializer import FilmListSerializer, FilmDetailSerializer, LikeSerializer, CommentSerializer, \
    CommentUpdateSerializer, CommentDeleteSerializer, CommentListSerializer


class FilmListAPIView(ListAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmListSerializer

    @extend_schema(
        description='I love you',
        summary='I love you'
    )
    def get(self, request, *args, **kwargs):
        film_genre = request.GET.get('genre', None)
        if film_genre:
            self.queryset = self.queryset.filter(
                genre__name__icontainы=film_genre
            )
        film_director = request.GET.get('director', None)
        if film_director:
            self.queryset = self.queryset.filter(
                director__name__icontains=film_director
            )
        film_rating = request.GET.get('rating', None)
        if film_rating:
            self.queryset = self.queryset.filter(
                rating__in=[film_rating, film_rating]
            )
        film_status = request.GET.get('status', None)
        if film_status:
            self.queryset = self.queryset.filter(
                status__icontains=film_status
            )
        return super().get(request, *args, **kwargs)


class FilmDetailAPIView(RetrieveAPIView):
    queryset = Film.objects.all()
    serializer_class = FilmDetailSerializer
    permission_classes = [IsAuthenticated]

    def perform_create_like(self, film):
        # Создаем сериализатор для объекта лайка, используя данные из запроса
        serializer_like = LikeSerializer(data=self.request.data)
        # Проверяем, что данные валидны
        serializer_like.is_valid(raise_exception=True)
        # Сохраняем лайк, связывая его с пользователем и статьей
        serializer_like.save(user=self.request.user, film=film)

    def get(self, request, *args, **kwargs):
        # Вызываем метод get() суперкласса для получения статьи
        response = super().get(request, *args, **kwargs)
        # Получаем объект статьи
        film = self.get_object()
        # Получаем все лайки, связанные со статьей
        likes = film.likes.all()
        # Создаем сериализатор для списка лайков
        like_serializer = LikeSerializer(likes, many=True)
        # Получаем данные статьи, используя сериализатор для детального представления
        response_data = self.serializer_class(film).data
        # Добавляем данные о лайках в объект ответа
        response_data['likes'] = like_serializer.data
        # Возвращаем объект ответа, содержащий данные о статье и ее лайках
        return Response(response_data)


class LikeCreateAPIView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        film_id = self.request.data.get('film')
        film = Film.objects.get(id=film_id)
        serializer.save(
            user=self.request.user,
            film=film
        )


class LikedFilmAPIView(ListAPIView):
    serializer_class = FilmListSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        liked_articles = Film.objects.filter(likes__user=self.request.user)
        serializer = self.serializer_class(liked_articles, many=True)
        return Response(serializer.data)


class CommentCreateAPIView(CreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        film_id = self.request.data.get('film')
        film_text = self.request.data.get('text')
        film = Film.objects.get(id=film_id)
        serializer.save(
            user=self.request.user,
            film=film,
            text=film_text
        )


class CommentUpdateAPIView(UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentUpdateSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class CommentDeleteAPIView(DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentDeleteSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


class CommentListAPIView(ListAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentListSerializer
