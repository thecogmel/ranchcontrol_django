from django.urls import path

from . import views

urlpatterns = [
    path('listar/', views.listar_funcionarios, name='funcionarios'),
    path('adicionar/', views.adicionar_funcionarios, name='adicionar'),
]
