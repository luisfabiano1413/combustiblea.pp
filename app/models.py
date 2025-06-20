from django.db import models
from django.contrib.auth.models import User

class Vehiculo(models.Model):
    TIPO_CHOICES = [
        ('moto', 'Moto'),
        ('auto', 'Auto'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=10, choices=TIPO_CHOICES)
    imagen = models.ImageField(upload_to='vehiculos/')
    placa = models.CharField(max_length=15, unique=True)
    registrado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'tipo')  # Un usuario no puede registrar dos autos o dos motos

    def __str__(self):
        return f"{self.usuario.username} - {self.tipo}"

class CargaCombustible(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    vehiculo = models.ForeignKey(Vehiculo, on_delete=models.CASCADE)
    litros = models.DecimalField(max_digits=6, decimal_places=2)
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.litros}L - Bs {self.monto}"
