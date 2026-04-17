from django.urls import path

from .views import admin_home

app_name = "adminpage"

urlpatterns = [
    path("dashboard/", admin_home, name="dashboard"),
]
