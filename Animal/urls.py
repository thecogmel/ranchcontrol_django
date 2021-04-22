from django.urls import path

from . import views

app_name = "animal"

urlpatterns = [
    path('listar/', views.listar_animais, name='listar'),
    path('adicionar/', views.adicionar_animais, name='adicionar'),
    path('deletar/<int:pk>/', views.deletar_animal, name="deletar"),
    path('editar/<int:pk>', views.editar_animal, name="editar"),
]
