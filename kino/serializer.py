from rest_framework import serializers

from kino.models import Film, Comment, Like


class FilmListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Film
        fields = ['title', 'image', 'rating', 'status']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['text', 'user', 'created']


class FilmDetailSerializer(serializers.ModelSerializer):
    genre = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    director = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True
    )
    likes_count = serializers.SerializerMethodField()
    comment = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Film
        fields = ['title', 'description', 'trailer', 'year',
                  'genre', 'director', 'rating', 'image', 'likes_count', 'comment']

    def get_likes_count(self, obj):
        # В данном случае obj будет представлять одну конкретную статью
        # (экземпляр модели Article), для которой нужно подсчитать
        # количество лайков.
        return obj.likes.count()


class CommentListSerializer(serializers.ModelSerializer):
    film = serializers.SlugRelatedField(
        slug_field='title',
        read_only=True
    )
    user = serializers.SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = ['text', 'film', 'user']

class LikeSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        read_only=True,
        slug_field='username'
    )
    film = serializers.PrimaryKeyRelatedField(
        queryset=Film.objects.all()
    )

    class Meta:
        model = Like
        fields = ['user', 'film', 'created']


class CommentCreateSerializer(serializers.ModelSerializer):
    # user = serializers.SlugRelatedField(
    #     slug_field='username',
    #     read_only=True
    # )
    # film = serializers.SlugRelatedField(
    #     slug_field='title',
    #     read_only=True
    # )

    class Meta:
        model = Comment
        fields = '__all__'

    def create(self, validate_data):
        comments = Comment.objects.create(**validate_data)
        comments.save()
        return comments


class CommentUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['text']

    def save(self):
        comment = super().save()
        comment.save()
        return comment


class CommentDeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id']