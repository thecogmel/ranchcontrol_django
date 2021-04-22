from django.db import models
from Funcionario.models import Funcionario
from Animal.models import Animal

# Create your models here.


class Baias(models.Model):
    nome_baia = models.CharField(max_length=300, null=False)
    capacidade = models.PositiveIntegerField(null=False)
    definicao = models.TextField()
    Funcionarios = models.ManyToManyField(Funcionario)


    def __str__(self):
        return self.nome_baia
