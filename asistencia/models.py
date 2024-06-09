from django.db import models
from django.conf import settings


class Usuario(models.Model):
    nombre = models.CharField(max_length=100)
    imagen = models.ImageField(upload_to='usuarios', null=True, blank=True)

    def __str__(self):
        return self.nombre

class Asistencia(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha = models.DateTimeField(auto_now_add=True)
    imagen_capturada = models.ImageField(upload_to='asistencia', null=True, blank=True)

    def __str__(self):
        return f"Asistencia de {self.usuario.nombre} el {self.fecha}"
    
    