from django.contrib import admin
from django.urls import include, path
from settings import base

from apps.auths import views

urlpatterns = [
    path(base.ADMIN_SITE_URL, admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),

    path('', views.home, name='home'),
    path('home/', views.home, name='home'),
    path('sign_up/', views.RegisterView.as_view(), name='sign_up'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.LogoutView.as_view(), name='logout'),
    
    path('set-bot-code/', views.SetBotCodeView.as_view(), name='set-bot-code'),
]
