from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

#from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.db import connection
from collections import namedtuple

from django.contrib import messages

from .forms import FuncionarioForm


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def listar_funcionarios(request):
    with connection.cursor() as cursor:
        # Função SQL que se quer executar (SELECT, INSERT, DELETE, UPDATE, ...)
        # Parâmetros serão passados nos []
        cursor.execute("SELECT * FROM Funcionario_funcionario ORDER BY nome", [])
        #resultado = cursor.fetchall()

        # Função que permite acessar os atributos das tuplas da tabela resultante da query
        resultado = namedtuplefetchall(cursor)
    return render(request, 'Funcionario/listar.html',
            {'funcionarios': resultado}
            )
def adicionar_funcionarios(request):
    if request.method == 'POST':
        form = FuncionarioForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            funcao = form.cleaned_data['funcao']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Funcionario_funcionario (nome, funcao) "
                                "VALUES (%s, %s)",
                                [nome, funcao])
                resultado = cursor.fetchall()
            return redirect('funcionario:listar')
    else:
        form = FuncionarioForm()
    return render(request, 'Funcionario/adicionar.html',
                {'form': form}
                )

