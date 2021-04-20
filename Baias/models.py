from django.db import models
from Funcionario.models import Funcionario
from Animal.models import Animal

# Create your models here.


class Baias(models.Model):
    nome_baia = models.CharField(max_length=300, null=False)
    capacidade = models.PositiveIntegerField(null=False)
    definicao = models.TextField()

    
    def __str__(self):
        return self.nome_baia

class BaiasMTM(models.Model):
    nome_baias = models.ForeignKey(Baias, on_delete=models.RESTRICT, null=True)
    Animais = models.ForeignKey(Animal, on_delete=models.RESTRICT, null=True)
    Funcionaios = models.ManyToManyField(Funcionario)
