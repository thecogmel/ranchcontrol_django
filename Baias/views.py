from django.http import HttpResponse

from django.shortcuts import render, redirect
from django.urls import reverse_lazy

from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from django.db import connection
from collections import namedtuple

from django.contrib import messages

from .models import Baias

from .forms import BaiasForm
from .forms import UpdateForm

def namedtuplefetchall(cursor):
    desc = cursor.description
    nt_result = namedtuple('Result', [col[0] for col in desc])
    return [nt_result(*row) for row in cursor.fetchall()]


def listar_baias(request):
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM Baias_baias  ORDER BY id", [])
        #resultado = cursor.fetchall()

        resultado = namedtuplefetchall(cursor)
    return render(request, 'Baia/listar.html',
                  {'baias': resultado}
                  )
class listar_baias_lv(ListView):
    model = Baias
    template_name = "Baia/listar_lv.html"              

def adicionar_baia(request):
    if request.method == 'POST':
        form = BaiasForm(request.POST)
        if form.is_valid():
            nome_baia = form.cleaned_data['nome_baia']
            capacidade = form.cleaned_data['capacidade']
            definicao = form.cleaned_data['definicao']
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO Baias_baias (nome_baia, capacidade, definicao) "
                               "VALUES (%s, %s, %s)",
                               [nome_baia, capacidade, definicao])
                resultado = cursor.fetchall()
            return redirect('baias:listar')
    else:
        form = BaiasForm()
    return render(request, 'Baia/adicionar.html',
                  {'form': form}
                  )
class adicionar_baias_cv(CreateView):
    model = Baias
    template_name = "Baia/adicionar_cv.html"
    fields = ['nome_baia', 'capacidade', 'definicao', 'Funcionarios' ]
    success_url = reverse_lazy('baias:listar_lv')

    def form_valid(self, form):
        if Baias.objects.filter(nome_baia = form.cleaned_data['nome_baia']):
            messages.add_message(self.request, messages.WARNING,
                                 "Já existe uma Baia com esse nome.")
            return self.render_to_response(self.get_context_data(form=form))
        else:
            return super(adicionar_baias_cv, self).form_valid(form)                

def deletar_baia(request, pk):
    if request.method == 'POST':
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Baias_baias WHERE id=%s", [pk])
            nome_baia = cursor.fetchall()[0][1]

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Baias_baias_Funcionarios WHERE baias_id=%s", [pk])
            resultado_baia_id = cursor.fetchall()
            cursor.execute("SELECT * FROM Animal_animal WHERE baia_id=%s", [pk])
            resultado_animal_baia_id = cursor.fetchall()

        if len(resultado_baia_id and resultado_animal_baia_id ) == 0:
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Baias_baias WHERE id=%s", [pk])
            messages.add_message(request, messages.ERROR, 'Baia ' + nome_baia + ' deletado com sucesso.')
            return redirect('baias:listar')

        else:
            if len(resultado_baia_id) > 0:
                with connection.cursor() as cursor:
                    cursor.execute("DELETE FROM Baias_baias_Funcionarios WHERE baias_id=%s", [pk])
                messages.add_message(request, messages.ERROR, 'Funcionários desvinculados da ' + nome_baia + '.')
            if len(resultado_animal_baia_id) > 0:
                with connection.cursor() as cursor:
                  cursor.execute("UPDATE Animal_animal SET baia_id=null "
                                "WHERE baia_id=%s",
                                  [pk])
                messages.add_message(request, messages.ERROR, 'Animais desvinculados da ' + nome_baia + '.')
            with connection.cursor() as cursor:
                cursor.execute("DELETE FROM Baias_baias WHERE id=%s", [pk])
            messages.add_message(request, messages.ERROR, 'Baia ' + nome_baia + ' deletado com sucesso.')
            return redirect('baias:listar')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Baias_baias WHERE id=%s", [pk])
            resultado = namedtuplefetchall(cursor)
        return render(request, "Baia/confirmar_deletar.html", {'baia': resultado[0]})
class deletar_baia_dv(DeleteView):
    model = Baias
    template_name = "Baia/confirmar_deletar_dv.html"
    success_url = reverse_lazy('baias:listar_lv')
 

def editar_baia(request, pk):
    if request.method == 'POST':
        form = UpdateForm(request.POST)
        if form.is_valid():
            nome_baia = form.cleaned_data['nome_baia']
            capacidade = form.cleaned_data['capacidade']
            definicao = form.cleaned_data['definicao']

            with connection.cursor() as cursor:
                cursor.execute("UPDATE Baias_baias SET nome_baia=%s, capacidade=%s, "
                               "definicao=%s WHERE id=%s",
                                [nome_baia, capacidade, definicao, pk])
                resultado = cursor.fetchall()
            return redirect('baias:listar')
    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Baias_baias  WHERE id=%s", [pk])
            resultado_baia = namedtuplefetchall(cursor)
        form = UpdateForm(initial={'nome_baia': resultado_baia[0].nome_baia,
                                    'capacidade': resultado_baia[0].capacidade,
                                    'definicao': resultado_baia[0].definicao,
                                    })
    return render(request, 'Baia/editar.html',
                {'form': form}
                )

class editar_baia_uv(UpdateView):
    model = Baias
    fields = ['nome_baia', 'capacidade', 'definicao', 'Funcionarios' ]
    template_name = "Baia/editar_uv.html"
    success_url = reverse_lazy('baias:listar_lv')