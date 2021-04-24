from django.urls import path

from . import views

app_name = "funcionario"

urlpatterns = [
    path('listar/', views.listar_funcionarios, name='listar'),
    path('adicionar/', views.adicionar_funcionarios, name='adicionar'),
    path('deletar/<int:pk>/', views.deletar_funcionario, name="deletar"),
    path('editar/<int:pk>', views.editar_funcionario, name="editar"),
    path('listar_lv/', views.listar_funcionarios_lv.as_view(), name='listar_lv'),
    path('adicionar_cv/', views.adicionar_funcionarios_cv.as_view(), name='adicionar_cv'),
    path('deletar_dv/<int:pk>/', views.deletar_funcionario_dv.as_view(), name='deletar_dv'),
    path('editar_uv/<int:pk>', views.editar_funcionario_uv.as_view(), name="editar_uv"),
]
