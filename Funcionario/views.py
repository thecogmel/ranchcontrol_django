from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.db import connection
from collections import namedtuple

from django.contrib import messages

from .models import Funcionario

from .forms import FuncionarioForm
from .forms import UpdateForm


def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]

def listar_funcionarios(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Funcionario_funcionario ORDER BY id", [])
        #resultado = cursor.fetchall()

        resultado = namedtuplefetchall(cursor)
    return render(request, 'Funcionario/listar.html',
            {'funcionarios': resultado}
            )
class listar_funcionarios_lv(ListView):
    model = Funcionario
    template_name = "Funcionario/listar_lv.html"

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
class adicionar_funcionarios_cv(CreateView):
    model = Funcionario
    template_name = "Funcionario/adicionar_cv.html"
    fields = ['nome', 'funcao']
    success_url = reverse_lazy('funcionario:listar_lv')

    def form_valid(self, form):
        if Funcionario.objects.filter(nome = form.cleaned_data['nome']):
            messages.add_message(self.request, messages.WARNING,
                                 "Já existe um funcionario com esse nome.")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super(adicionar_funcionarios_cv, self).form_valid(form)                

def deletar_funcionario(request, pk):
    if request.method == 'POST':

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Funcionario_funcionario WHERE id=%s", [pk])
            nome_funcionario = cursor.fetchall()[0][1]

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Baias_baias_Funcionarios WHERE funcionario_id=%s", [pk])
            resultado = cursor.fetchall()

        if len(resultado) == 0:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Baias_baias_Funcionarios WHERE funcionario_id=%s", [pk])
                cursor.execute("DELETE FROM Funcionario_funcionario WHERE id=%s", [pk])
            messages.add_message(request, messages.ERROR, 'Funcionario ' + nome_funcionario + ' deletado com sucesso.')
            return redirect('funcionario:listar')

        else:
            messages.add_message(request, messages.ERROR, 'Não é possível deletar o funcionario ' + nome_funcionario + '. Há baias associados a este produto.')
            return redirect('funcionario:listar')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Funcionario_funcionario WHERE id=%s", [pk])
            resultado = namedtuplefetchall(cursor)
        return render(request, "Funcionario/confirmar_deletar.html", {'funcionario': resultado[0]})

class deletar_funcionario_dv(DeleteView):
    model = Funcionario
    template_name = "Funcionario/confirmar_deletar_dv.html"
    success_url = reverse_lazy('funcionario:listar')


def editar_funcionario(request, pk):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['nome']
            funcao = form.cleaned_data['funcao']

            with connection.cursor() as cursor:
                cursor.execute("UPDATE Funcionario_funcionario SET nome=%s, funcao=%s WHERE id=%s",
                                [nome, funcao, pk])
                resultado = cursor.fetchall()
            return redirect('funcionario:listar')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Funcionario_funcionario WHERE id=%s", [pk])
            resultado_funcionario = namedtuplefetchall(cursor)
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Baias_baias_Funcionarios WHERE id=%s", [resultado_funcionario[0].id])
            resultado_baias = namedtuplefetchall(cursor)
        form = UpdateForm(initial={'nome': resultado_funcionario[0].nome,
                                    'funcao': resultado_funcionario[0].funcao,
                                    })
    return render(request, 'Funcionario/editar.html',
                {'form': form}
                )

class editar_funcionario_uv(UpdateView):
    model = Funcionario
    fields = ['nome', 'funcao']
    template_name = "Funcionario/editar_uv.html"
    success_url = reverse_lazy('funcionario:listar')
