from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework.authtoken import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api-token-auth/', views.obtain_auth_token),
    re_path(r"", include("task_manager.urls")),
]
