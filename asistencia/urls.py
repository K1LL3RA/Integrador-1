from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('capturar/', views.capturar, name='capturar'),
    path('agregar-usuario/', views.agregar_usuario, name='agregar_usuario'),
    path('alumnos/', views.vista_alumnos, name='alumnos'),
    path('lobby/', views.lobby_view, name='lobby'),
    path('index/', views.index_view, name='index'),
]