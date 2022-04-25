from django.urls import path
from .views import deleteItem, home
from . import views

urlpatterns = [
    path("", home, name="home"),
    path('view-passwords', views.passwords, name="passwords"),
    path('delete-item/<int:id>/', views.deleteItem, name="delete-item"),
]