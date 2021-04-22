from django import forms
from django.db import connection

from django.contrib import messages

from django.core.exceptions import ValidationError

from .models import Baias

class BaiasForm(forms.ModelForm):
    class Meta:
        model = Baias
        fields = ['nome_baia', 'capacidade', 'definicao' ]

    def clean(self):
        cleaned_data = super().clean()
        # Pega o nome que foi adicionado no formulário
        nome_baia = cleaned_data.get("nome_baia")

        # Seleciona se há funcionarios com este mesmo nome
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Baias_baias WHERE nome_baia=%s", [nome_baia])
            resultado_baia = cursor.fetchall()

        # Se a lista não foi vazia, há animal com o mesmo nome
        if (len(resultado_baia) != 0):
            raise ValidationError("Já foi criado uma baia com este nome. Escolha outro nome.")

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Baias
        fields = ['nome_baia', 'capacidade', 'definicao']

    def clean(self):
        cleaned_data = super().clean()
        # Pega o nome que foi adicionado no formulário
        nome_baia = cleaned_data.get("nome_baia")

        # Seleciona se há animals com este mesmo nome
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Baias_baias WHERE nome_baia=%s", [nome_baia])
            resultado_baia = cursor.fetchall()

        #implementar aviso de nome igual

