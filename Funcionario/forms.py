from django import forms
from django.db import connection

from django.core.exceptions import ValidationError

from .models import Funcionario

class FuncionarioForm(forms.ModelForm):
    class Meta:
        model = Funcionario
        fields = ['nome', 'funcao']

    def clean(self):
        cleaned_data = super().clean()
        # Pega o nome que foi adicionado no formulário
        nome = cleaned_data.get("nome")

        # Seleciona se há funcionarios com este mesmo nome
        with connection.cursor() as cursor:
            cursor.execute("SELECT * FROM Funcionario_funcionario WHERE nome=%s", [nome])
            resultado_funcionario = cursor.fetchall()

        # Se a lista não foi vazia, há funcionario com o mesmo nome
        if (len(resultado_funcionario) != 0):
            raise ValidationError("Já foi criado um funcionario com este nome. Escolha outro nome.")
