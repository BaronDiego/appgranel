import datetime
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
ESTADO = (
    ('EJ', 'En ejecución'),
    ('F', 'Finalizado'),
    ('S', 'Suspendido'),
    ('C', 'Cancelado'),
)

TERMINAL = (
    ('BUN', 'Buenaventura'),
    ('CTG', 'Cartagena'),
    ('BOG', 'Bogotá'),
)

class Proyecto(models.Model):
    nombre = models.CharField(max_length=250)
    objeto = models.TextField()
    contratista = models.CharField(max_length=150)
    numero_contrato = models.IntegerField(verbose_name="Número Contrato")
    estado = models.CharField(max_length=2, choices=ESTADO)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    terminal = models.CharField(max_length=3, choices=TERMINAL)
    valor_proyecto = models.IntegerField(blank=True, null=True)
    programado = models.FloatField(max_length=5, blank=True, null=True)
    avance = models.FloatField(max_length=5, blank=True, null=True)
    responsable = models.CharField(max_length=50, blank=True)
    interventoria = models.BooleanField(default=False)
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True, verbose_name="Usuario que modifica")

    class Meta:
        ordering = ['-creado']

    def __str__(self):
        return self.nombre

    def duracion(self):
        duracion = self.fecha_fin - self.fecha_inicio
        return duracion.days


class Pago(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    fecha_pago = models.DateField()
    valor_pago = models.IntegerField(blank=True, null=True)
    concepto_pago = models.CharField(max_length=150)
    numero_factura = models.CharField(max_length=15, blank=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-creado']


class Documento(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    documento = models.FileField(upload_to='documentos/%Y/%m/%d/')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado']


class Imagen(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    imagen = models.ImageField(upload_to='imagenes/%Y/%m/%d/')
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['-creado']


class Cambio(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=150)
    afecta_tiempo = models.BooleanField(default=False, verbose_name="Afecta en Tiempo")
    duracion = models.IntegerField(blank=True, null=True)
    afecta_costo = models.BooleanField(default=False, verbose_name="Afecta en Costo")
    costo = models.IntegerField(blank=True, null=True)
    fecha_de_cambio = models.DateField()
    genero_documento = models.BooleanField(default=False)
    nombre_documento = models.CharField(max_length=150)
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-creado']


class Actividad(models.Model):
    proyecto = models.ForeignKey(Proyecto, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=150)
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    actualizado = models.DateTimeField(auto_now=True)
    programado = models.FloatField(max_length=5, blank=True, null=True)
    avance = models.FloatField(max_length=5, blank=True, null=True)
    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)
    uc = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuario que Crea")
    um = models.IntegerField(blank=True, null=True)

    class Meta:
        ordering = ['creado']

    def __str__(self):
        return self.nombre

    def duracion(self):
        duracion = (self.fecha_fin - self.fecha_inicio) + datetime.timedelta(days=1)
        return duracion.days

    