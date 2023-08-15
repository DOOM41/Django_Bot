from django.contrib import admin
from django.urls import include, path
from settings import base

urlpatterns = [
    path(base.ADMIN_SITE_URL, admin.site.urls),
    path('api-auth/', include('rest_framework.urls'))
]
