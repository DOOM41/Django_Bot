from typing import Any
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
from auths.models import CustomUser
from auths.forms import RegisterForm, LoginForm


class RegisterView(FormView):
    template_name: str = 'auth/sign_up.html'
    form_class = RegisterForm
    success_url = reverse_lazy("home")

    def form_valid(self, form) -> HttpResponse:
        login = form.cleaned_data.get('login')
        first_name = form.cleaned_data.get('first_name')
        password = form.cleaned_data.get('password')
        user = CustomUser.objects.create_user(login, first_name, password)
        dj_login(self.request, user)
        return super().form_valid(form)


class LoginView(FormView):
    template_name: str = 'auth/login.html'
    form_class = LoginForm
    success_url = reverse_lazy("home")

    def form_valid(self, form) -> HttpResponse:
        login = form.cleaned_data.get('login')
        password = form.cleaned_data.get('password')
        user = dj_authenticate(login=login, password=password)
        if user:
            dj_login(self.request, user)
        return super().form_valid(form)


class LogoutView(View):
    template_name: str = 'auth/login.html'

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        dj_logout(request)
        return redirect('/login')


def home(request: HttpRequest) -> HttpResponse:
    return render(request, "core/home.html")
