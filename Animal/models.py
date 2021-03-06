from django.db import models

# Create your models here.


class Animal(models.Model):
    nome_animal = models.CharField(max_length=300, null=False)
    idade_animal = models.PositiveIntegerField(null=False)
    tipo_animal = models.CharField(max_length=300, null=False)
    peso_animal = models.DecimalField(max_digits=5,decimal_places=2)
    baia = models.ForeignKey("Baias.Baias", on_delete=models.CASCADE, null=True)
    obs = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.nome_animal + " - " + self.tipo_animal
