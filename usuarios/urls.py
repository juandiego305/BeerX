from django.urls import path
from .views import RegistrarUsuarioView

urlpatterns = [
    path('register/', RegistrarUsuarioView.as_view(), name='auth_register'),
]