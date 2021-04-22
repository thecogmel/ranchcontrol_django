from django.urls import path

from . import views

app_name = "funcionario"

urlpatterns = [
    path('listar/', views.listar_funcionarios, name='listar'),
    path('adicionar/', views.adicionar_funcionarios, name='adicionar'),
    path('deletar/<int:pk>/', views.deletar_funcionario, name="deletar"),
    path('editar/<int:pk>', views.editar_funcionario, name="editar"),
]
