from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Resultados(models.Model):
    description = models.CharField(max_length=100)
    Porosity = models.CharField(max_length=100)
    Permeability = models.CharField(max_length=100)
    API = models.CharField(max_length=100)