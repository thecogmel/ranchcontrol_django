from django.db import models

# Create your models here.


class Baias(models.Model):
    nome_baia = models.CharField(max_length=300, null=False)
    capacidade = models.PositiveIntegerField(null=False)
    definicao = models.TextField()
    id_funcionario_responsavel = models.PositiveIntegerField()
    nome_funcionario = models.CharField(max_length=300, null=False)

    def __str__(self):
        return self.nome_baia
