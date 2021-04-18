from django.db import models
# Create your models here.
class Funcionario(models.Model):
  nome = models.CharField(max_length=300, null=False)
  funcao = models.CharField(max_length=300, null=False)
  def __str__(self):
    return self.nome + " - " + self.funcao;