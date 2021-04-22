from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

#from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.db import connection
from collections import namedtuple

from django.contrib import messages

from .forms import AnimalForm
from .forms import UpdateForm


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def listar_animais(request):
    with connection.cursor() as cursor:
        # Função SQL que se quer executar (SELECT, INSERT, DELETE, UPDATE, ...)
        # Parâmetros serão passados nos []
        cursor.execute("SELECT * FROM Animal_animal  ORDER BY id", [])
        #resultado = cursor.fetchall()

        # Função que permite acessar os atributos das tuplas da tabela resultante da query
        resultado = namedtuplefetchall(cursor)
    return render(request, 'Animal/listar.html',
                  {'animais': resultado}
                  )


def adicionar_animais(request):
    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            nome_animal = form.cleaned_data['nome_animal']
            idade_animal = form.cleaned_data['idade_animal']
            tipo_animal = form.cleaned_data['tipo_animal']
            peso_animal = form.cleaned_data['peso_animal']
            obs = form.cleaned_data['obs']
            baia = form.cleaned_data['baia']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Animal_animal (nome_animal, idade_animal, tipo_animal, "
                               "peso_animal, obs, baia_id) "
                               "VALUES (%s, %s, %s, %s, %s, %s)",
                               [nome_animal, idade_animal, tipo_animal, peso_animal, obs, baia.id])
                resultado = cursor.fetchall()
            return redirect('animal:listar')
    else:
        form = AnimalForm()
    return render(request, 'Animal/adicionar.html',
                  {'form': form}
                  )


def deletar_animal(request, pk):
    with connection.cursor() as cursor:
        cursor.execute("DELETE FROM Animal_animal WHERE id=%s", [pk])
    return redirect('animal:listar')


def editar_animal(request, pk):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            nome_animal = form.cleaned_data['nome_animal']
            idade_animal = form.cleaned_data['idade_animal']
            tipo_animal = form.cleaned_data['tipo_animal']
            peso_animal = form.cleaned_data['peso_animal']
            obs = form.cleaned_data['obs']
            baia = form.cleaned_data['baia']

            with connection.cursor() as cursor:
                cursor.execute("UPDATE Animal_animal SET nome_animal=%s, idade_animal=%s, "
                               "tipo_animal=%s, peso_animal=%s, obs=%s, baia_id=%s "
                               "WHERE id=%s",
                                [nome_animal, idade_animal, tipo_animal, peso_animal, obs, baia.id, pk])
                resultado = cursor.fetchall()
            return redirect('animal:listar')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Animal_animal  WHERE id=%s", [pk])
            resultado_animal = namedtuplefetchall(cursor)
        form = UpdateForm(initial={'nome_animal': resultado_animal[0].nome_animal,
                                    'idade_animal': resultado_animal[0].idade_animal,
                                    'tipo_animal': resultado_animal[0].tipo_animal,
                                    'peso_animal': resultado_animal[0].peso_animal,
                                    'obs': resultado_animal[0].obs,
                                    'baia': resultado_animal[0].baia_id,
                                    })
    return render(request, 'Funcionario/editar.html',
                {'form': form}
                )
