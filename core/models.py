from django.db import models

import uuid

# Create your models here.
class BasePadraoAbstract(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    data_criacao = models.DateField('Data de inclusão da foto',auto_now_add=True, editable=False)
    data_alteracao = models.DateField('Data de inclusão da foto',auto_now=True, editable=False)
    ativo = models.BooleanField('Ativo?',default=True, blank=True)

    class Meta:
        abstract = True
        ordering = ['-ativo', '-data_alteracao' ]
        # ordering = ['data_alteracao']
