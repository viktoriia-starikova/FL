# from django.shortcuts import render, redirect
# from .form import MyUserReg, ProfileImage,UserUpdateForm
# from django.contrib import messages
# from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from .models import Profile
from .serializers import *
from rest_framework import permissions, generics, mixins, viewsets
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework.parsers import FileUploadParser, MultiPartParser, FormParser
import logging

logger = logging.getLogger('FreelanceExchange')

class ProfileUser(APIView):
    """Вывод профиля пользователя"""
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        ser = ProfileSerializer(Profile.objects.get(user=request.user))
        return Response(ser.data)

class ProfDetail(APIView):
    """Вывод публичного профиля пользователя"""
    permission_classes = [permissions.AllowAny]

    def get_object(self, pk):
        try:
            return Profile.objects.get(user=User.objects.get(pk=pk))
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        prof = self.get_object(pk)
        if(prof.user==request.user):
            serializer = ProfileSerializer(prof)
        else:
            serializer = PublicProfileSerializer(prof)
        return Response(serializer.data)

class RegUser(APIView):
    """Регистрация нового юзера"""
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = RegSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=201)
        else:
            logger.error('Пользователь не может быть зарегистрирован, данные введены некорректно: RegUser')
            return Response(serializer.errors, status=400)


class UpdateProfile(APIView):
    """Редактирование аватара"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return Profile.objects.get(pk=pk)
        except Profile.DoesNotExist:
            raise Http404

    def post(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RedactIMG(instance=snippet, data=request.data, partial=True)
        if serializer.is_valid():
            if "img" in request.FILES:
                serializer.save(img=request.data["img"])
                serializer.save()
                return Response(serializer.data,status=201)
            return Response(serializer.errors,status=400)
        else:
            logger.error('Аватар не может быть обновлен: ImageView')
            return Response(serializer.errors,status=400)

class RedactProfile(APIView):
    """Редактирование профиля"""
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self, pk):
        try:
            return User.objects.get(pk=pk)
        except User.DoesNotExist:
            raise Http404


    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = RedactSerialiser(instance=snippet, data=request.data, partial=True)
        if serializer.is_valid():
            if (self.request.user.username == snippet.username):
                serializer.save()
                return Response(serializer.data)
        logger.error('Профиль не может быть обновлен: UpdateProfile')
        return Response(serializer.errors, status=400)
