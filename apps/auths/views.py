# Python
from typing import Any

# Django
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.contrib.auth import (
    authenticate as dj_authenticate,
    login as dj_login,
    logout as dj_logout,
)
from django.views.generic import FormView
from django.http import HttpRequest, HttpResponse

# DRF
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status

# Apps
from auths.models import CustomUser
from auths.forms import RegisterForm, LoginForm
from auths.serializers import CustomUserSerializer

class RegisterView(FormView):
    template_name: str = 'auth/sign_up.html'
    form_class = RegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form) -> HttpResponse:
        login = form.cleaned_data.get('login')
        first_name = form.cleaned_data.get('first_name')
        password = form.cleaned_data.get('password')
        CustomUser.objects.create_user(login, first_name, password)
        return super().form_valid(form)


class LoginView(FormView):
    template_name: str = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form) -> HttpResponse:
        login = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')
        user: CustomUser = dj_authenticate(login=login, password=password)
        if user:
            dj_login(self.request, user)
            CustomUser.objects.set_code(user)
        return super().form_valid(form)


class LogoutView(View):
    template_name: str = 'auth/login.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        dj_logout(request)
        return redirect('/login')

class SetBotCodeView(APIView):
    def post(self, request: Request, format=None):
        serializer = CustomUserSerializer(data=request.data)
        
        if serializer.is_valid():
            try:
                chat_id = serializer.validated_data['chat_id']
                bot_code = serializer.validated_data['bot_code']
                user: CustomUser = CustomUser.objects.get(bot_code=bot_code)
                if user.chat_id:
                    return Response({'error': 'Пользователь уже иницирован!'}, status=status.HTTP_400_BAD_REQUEST)
                CustomUser.objects.set_chat_id(user, chat_id)
                return Response(status=status.HTTP_200_OK)
            except CustomUser.DoesNotExist:
                return Response({'error': 'Пользователь не найден'}, status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")
