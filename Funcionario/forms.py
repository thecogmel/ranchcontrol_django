from django import forms
from django.db import connection

from django.contrib import messages

from django.core.exceptions import ValidationError

from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'funcao']

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Funcionario_funcionario WHERE nome=%s", [nome])
            resultado_funcionario = cursor.fetchall()

        if (len(resultado_funcionario) != 0):
            raise ValidationError("Já foi criado um funcionario com este nome. Escolha outro nome.")

class UpdateForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'funcao']

    def clean(self):
        cleaned_data = super().clean()
        nome = cleaned_data.get("nome")

        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Funcionario_funcionario WHERE nome=%s", [nome])
            resultado_funcionario = cursor.fetchall()


