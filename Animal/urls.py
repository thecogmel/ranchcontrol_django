from django.urls import path

from . import views

app_name = "animal"

urlpatterns = [
    path('listar/', views.listar_animais, name='listar'),
    path('adicionar/', views.adicionar_animais, name='adicionar'),
    path('deletar/<int:pk>/', views.deletar_animal, name="deletar"),
    path('editar/<int:pk>', views.editar_animal, name="editar"),
    path('listar_lv/', views.listar_animais_lv.as_view(), name='listar_lv'),
    path('adicionar_cv/', views.adicionar_animal_cv.as_view(), name='adicionar_cv'),
    path('deletar_dv/<int:pk>/', views.deletar_animal_dv.as_view(), name='deletar_dv'),
    path('editar_uv/<int:pk>', views.editar_animal_uv.as_view(), name="editar_uv"),
]
