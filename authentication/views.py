from django.http import JsonResponse
from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import CreateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from authentication.models import User
from authentication.serializers import UserCreateSerializer, UserDetailSerializer, UserDeleteSerializer
from kino.permissions import IsAuthorOrReadOnly


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserCreateSerializer


class Logout(APIView):
    def post(self, request):
        request.user.auth_token.delete()
        return JsonResponse(status=status.HTTP_200_OK)


class UserDetailAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserDetailSerializer
    permission_classes = [IsAuthenticated]


class UserDeleteAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserDeleteSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]

