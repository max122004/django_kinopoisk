from django.db import models

from authentication.models import User


class Genre(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')


class Director(models.Model):
    name = models.CharField(max_length=100, verbose_name='Имя артистов')


class Film(models.Model):
    STATUS = [
        ('premium', 'Полный доступ'),
        ('default', 'Обычный доступ')
    ]

    title = models.CharField(max_length=100, verbose_name='Название фильма')
    description = models.CharField(max_length=1000, verbose_name='Описание фильма')
    trailer = models.URLField(max_length=1000, verbose_name='Трейлер фильма')
    year = models.IntegerField(verbose_name='Год создания')
    genre = models.ForeignKey(Genre, null=True, on_delete=models.SET_NULL, verbose_name='Жанр фильма')
    director = models.ForeignKey(Director, null=True, on_delete=models.SET_NULL, verbose_name='Артисты фильма')
    status = models.CharField(max_length=20, choices=STATUS, default='default', verbose_name='Доступ фильма')
    rating = models.IntegerField(verbose_name='Рейтинг фильма')
    image = models.ImageField(upload_to="films/", null=True, blank=True)


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='likes')
    created = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    text = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    film = models.ForeignKey(Film, on_delete=models.CASCADE, related_name='comment')
    created = models.DateTimeField(auto_now_add=True)