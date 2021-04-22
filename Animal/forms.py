from django import forms
from django.db import connection

from django.contrib import messages

from django.core.exceptions import ValidationError

from .models import Animal

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome_animal', 'idade_animal', 'tipo_animal', 'peso_animal', 'obs', 'baia']

    def clean(self):
        cleaned_data = super().clean()
        # Pega o nome que foi adicionado no formulário
        nome_animal = cleaned_data.get("nome_animal")

        # Seleciona se há funcionarios com este mesmo nome
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Animal_animal WHERE nome_animal=%s", [nome_animal])
            resultado_animal = cursor.fetchall()

        # Se a lista não foi vazia, há animal com o mesmo nome
        if (len(resultado_animal) != 0):
            raise ValidationError("Já foi criado um animal com este nome. Escolha outro nome.")

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Animal
        fields = ['nome_animal', 'idade_animal', 'tipo_animal', 'peso_animal', 'obs', 'baia']

    def clean(self):
        cleaned_data = super().clean()
        # Pega o nome que foi adicionado no formulário
        nome_animal = cleaned_data.get("nome_animal")

        # Seleciona se há animals com este mesmo nome
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Animal_animal WHERE nome_animal=%s", [nome_animal])
            resultado_animal = cursor.fetchall()

        #implementar aviso de nome igual

