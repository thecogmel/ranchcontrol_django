from django.urls import path

from . import views

app_name = "baias"

urlpatterns = [
    path('listar/', views.listar_baias, name='listar'),
    path('adicionar/', views.adicionar_baia, name='adicionar'),
    path('deletar/<int:pk>/', views.deletar_baia, name="deletar"),
    path('editar/<int:pk>', views.editar_baia, name="editar"),
]
