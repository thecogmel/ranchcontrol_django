from django.urls import path

from . import views

app_name = "baias"

urlpatterns = [
    path('listar/', views.listar_baias, name='listar'),
    path('adicionar/', views.adicionar_baia, name='adicionar'),
    path('deletar/<int:pk>/', views.deletar_baia, name="deletar"),
    path('editar/<int:pk>', views.editar_baia, name="editar"),
    path('listar_lv/', views.listar_baias_lv.as_view(), name='listar_lv'),
    path('adicionar_cv/', views.adicionar_baias_cv.as_view(), name='adicionar_cv'),
    path('deletar_dv/<int:pk>/', views.deletar_baia_dv.as_view(), name='deletar_dv'),
    path('editar_uv/<int:pk>', views.editar_baia_uv.as_view(), name="editar_uv"),
]
