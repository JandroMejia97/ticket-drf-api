from django.db import models
from django.core import validators
from django.conf import settings
from django.dispatch import receiver
from django.contrib.auth.models import AbstractUser

from rest_framework.authtoken.models import Token

from phonenumber_field.modelfields import PhoneNumberField

@receiver(models.signals.post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Rol(models.IntegerChoices):
    CAJERO = 1, 'CAJERO'
    USUARIO = 2, 'USUARIO'
    ADMINISTRADOR = 3, 'ADMINISTRADOR'


class Dia(models.IntegerChoices):
    DOMINGO = 1, 'DOMINGO'
    LUNES = 2, 'LUNES'
    MARTES = 3, 'MARTES'
    MIERCOLES = 4, 'MIÉRCOLES'
    JUEVES = 5, 'JUEVES'
    VIERNES = 6, 'VIERNES'
    SABADO = 7, 'SÁBADO'


class Estado(models.IntegerChoices):
    ESPERA = 1, 'ESPERA'
    ACTIVO = 2, 'ACTIVO'
    PASO = 3, 'PASO'
    VENCIDO = 4, 'VENCIDO'
    RETIRADO = 5, 'RETIRADO'


class Usuario(AbstractUser):
    telefono = PhoneNumberField(
        null=True,
        blank=True,
        default=None,
        verbose_name='número de teléfono',
        help_text='Ingrese su número de teléfono en el formato +41524204242'
    )
    rol = models.PositiveSmallIntegerField(
        choices=Rol.choices,
        default=Rol.USUARIO,
        blank=False,
        null=False,
        validators=(
            validators.MinValueValidator(1, 'La opción seleccionada es inválida'),
            validators.MaxValueValidator(3, 'La opción seleccionada es inválida'),
        ),
        verbose_name='rol',
        help_text='Seleccione el ROL del usuario.'
    )
    sucursal = models.ForeignKey(
        to='Sucursal',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        verbose_name='sucursal',
        help_text='Seleccione una sucursal si este usuario tiene el rol "CAJERO".'
    )

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'usuario'
        verbose_name_plural = 'usuarios'
        ordering = ['rol', 'username']


class Departamento(models.Model):
    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='nombre',
        help_text='Ingrese el nombre de este departamento.'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'departamento'
        verbose_name_plural = 'departamentos'
        ordering = ['nombre']


class Municipio(models.Model):
    nombre = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='nombre',
        help_text='Ingrese el nombre de este municipio.'
    )
    departamento = models.ForeignKey(
        to=Departamento,
        on_delete=models.CASCADE,
        verbose_name='departamento',
        help_text='Seleccione el departamento'
    )

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = 'municipio'
        verbose_name_plural = 'municipios'
        ordering = ['departamento', 'nombre']


class TipoEmpresa(models.Model):
    tipo = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        verbose_name='tipo',
        help_text='Ingrese el tipo de empresa.'
    )

    def __str__(self):
        return self.tipo
    
    class Meta:
        verbose_name = 'tipo de empresa'
        verbose_name_plural = 'tipos de empresa'
        ordering = ['tipo']

class Empresa(models.Model):
    nombre = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='nombre',
        help_text='Ingrese el nombre de la empresa.'
    )
    nombre_corto = models.CharField(
        max_length=50,
        blank=False,
        null=False,
        verbose_name='nombre corto',
        help_text='Ingrese el nombre corto de la empresa.'
    )
    nit = models.CharField(
        max_length=17,
        blank=False,
        null=False,
        verbose_name='nit',
        help_text='Ingrese el NIT de la empresa.'
    )
    tipo = models.ForeignKey(
        to=TipoEmpresa,
        on_delete=models.DO_NOTHING,
        default=None,
        null=True,
        blank=False,
        verbose_name='tipo de empresa',
        help_text='Seleccione el tipo de empresa.'
    )
    administrador = models.ForeignKey(
        to=Usuario,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        default=None,
        verbose_name='administrador',
        help_text='Seleccione el administrador del sistema para esta empresa.'
    )

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'empresa'
        verbose_name_plural = 'empresas'
        ordering = ['nombre', 'nombre_corto']
    

class TipoCola(models.Model):
    tipo = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        verbose_name='tipo de cola',
        help_text='Ingrese el nombre de este tipo de cola.'
    )
    descripcion = models.CharField(
        max_length=150,
        null=True,
        blank=True,
        default=None,
        verbose_name='descripcion',
        help_text='Ingrese una descripción.'
    )
    capacidad = models.PositiveSmallIntegerField(
        blank=False,
        null=False,
        verbose_name='capacidad',
        help_text='Ingrese la capacidad máxima de esta cola.'
    )
    empresa = models.ForeignKey(
        to=Empresa,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='empresa',
        help_text='Selecccione la empresa a la que pertenece este tipo de cola.'
    )

    def __str__(self):
        return '%s - %s' % (self.empresa, self.tipo)
    
    class Meta:
        verbose_name = 'tipo de cola'
        verbose_name_plural = 'tipos de cola'
        ordering = ['empresa', 'capacidad', 'tipo']


class  Sucursal(models.Model):
    nombre = models.CharField(
        max_length=150,
        blank=False,
        null=False,
        verbose_name='nombre',
        help_text='Ingrese el nombre de la empresa.'
    )
    latitud = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=6,
        max_digits=9,
        validators=(
            validators.MinValueValidator(-90.00000),
            validators.MaxValueValidator(90.00000)
        ),
        help_text=
            'La latitud está dada en grados decimales, entre 0° '\
            'y 90 ° en el hemisferio Norte y entre 0° y -90° en '\
            'el hemisferio Sur',
        verbose_name='latitud'
    )
    longitud = models.DecimalField(
        blank=True,
        null=True,
        decimal_places=6,
        max_digits=9,
        validators=[
            validators.MinValueValidator(-180.00000),
            validators.MaxValueValidator(180.00000)
        ],
        help_text=
            'La longitud está dada en grados decimales, entre 0° '\
            'y 180°, al este del meridiano de Greenwich y entre 0° '\
            'y -180°, al oeste del meridiano de Greenwich.',
        verbose_name='longitud'
    )
    direccion = models.CharField(
        max_length=200,
        blank=True,
        null=True,
        verbose_name='dirección',
        help_text='Ingrese la dirección.'
    )
    empresa = models.ForeignKey(
        to=Empresa,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='empresa',
        help_text='Selecccione la empresa a la que pertenece esta sucursal.'
    )
    municipio = models.ForeignKey(
        to=Municipio,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='municipio',
        help_text='Seleccione el municipio en el que se encuentra esta sucursal.'
    )

    def __str__(self):
        return self.nombre
    
    class Meta:
        verbose_name = 'sucursal'
        verbose_name_plural = 'sucursales'
        ordering = ['empresa', 'municipio', 'nombre']
    

class Horario(models.Model):
    hora_apertura = models.TimeField()
    hora_cierre = models.TimeField()
    dia = models.IntegerField(
        choices=Dia.choices,
        default=Dia.LUNES,
        blank=False,
        null=False,
        validators=(
            validators.MinValueValidator(1, 'La opción seleccionada es inválida'),
            validators.MaxValueValidator(7, 'La opción seleccionada es inválida'),
        ),
        verbose_name='rol',
        help_text='Seleccione el día en que se tiene este horario.'
    )
    sucursal = models.ForeignKey(
        to=Sucursal,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='sucursal',
        help_text='Seleccione una sucursal para este horario.'
    )

    def __str__(self):
        return '%s de %s - %s' % (
            self.dia,
            self.hora_apertura,
            self.hora_cierre
        )
    
    class Meta:
        verbose_name = 'horario'
        verbose_name_plural = 'horarios'
        ordering = ['sucursal', 'dia', 'hora_apertura', 'hora_cierre']


class Cola(models.Model):
    fecha = models.DateField(
        blank=False,
        null=False,
        verbose_name='fecha',
        help_text='Fecha en la que se habilitará esta cola.'
    )
    tipo_cola = models.ForeignKey(
        to=TipoCola,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=False,
        verbose_name='tipo de cola',
        help_text='Seleccione el tipo de esta cola.'
    )
    sucursal = models.ForeignKey(
        to=Sucursal,
        on_delete=models.CASCADE,
        null=False,
        blank=False,
        verbose_name='sucursal',
        help_text='Seleccione la sucursal para la que habilitará esta cola.'
    )
    horario = models.ForeignKey(
        to=Horario,
        on_delete=models.DO_NOTHING,
        null=True,
        blank=False,
        verbose_name='horario',
        help_text='Seleccione el horario en el cual esta cola estará habilitada'
    )

    def __str__(self):
        return '%s - %s - %s' % (
            self.sucursal,
            self.horario,
            self.tipo_cola
        )
    
    class Meta:
        verbose_name = 'cola'
        verbose_name_plural = 'colas'
        ordering = [
            'fecha',
            'sucursal',
            'horario',
            'tipo_cola'
        ]


class Ticket(models.Model):
    numero = models.CharField(
        max_length=10,
        blank=False,
        null=False,
        verbose_name='número',
        help_text='Ingrese el número del ticket.'
    )
    estado = models.PositiveSmallIntegerField(
        choices=Estado.choices,
        default=Estado.ESPERA,
        blank=False,
        null=False,
        validators=(
            validators.MinValueValidator(1, 'La opción seleccionada es inválida'),
            validators.MaxValueValidator(5, 'La opción seleccionada es inválida'),
        ),
        verbose_name='estado',
        help_text='Seleccione el estado actual de este ticket.'
    )
    hora_generado = models.TimeField(
        auto_now_add=True,
        blank=True,
        null=False,
        verbose_name='hora de generación',
        help_text='Hora en la que se generó este ticket.'
    )
    cant_intentos = models.PositiveSmallIntegerField(
        default=1,
        blank=False,
        null=False,
        validators=(
            validators.MinValueValidator(1),
            validators.MaxValueValidator(3, 'Solo se permiten 3 intentos.'),
        ),
        verbose_name='cantidad de intentos',
        help_text='Ingrese la cantidad de intentos que se hizo para despachar este ticket.'
    )
    cola = models.ForeignKey(
        to=Cola,
        on_delete=models.CASCADE,
        blank=False,
        null=False,
        verbose_name='cola',
        help_text='Seleccione la cola a la que asignará este ticket.'
    )
    cliente = models.ForeignKey(
        to=Usuario,
        on_delete=models.DO_NOTHING,
        blank=False,
        null=True,
        verbose_name='cliente',
        related_name='cliente',
        help_text='Seleccione el usuario al que le asignará este ticket.'
    )
    cajero = models.ForeignKey(
        to=Usuario,
        on_delete=models.CASCADE,
        blank=False,
        null=True,
        verbose_name='cajero',
        related_name='cajero',
        help_text='Seleccione el cajero que despachó este ticket.'
    )

    def __str__(self):
        return '%s - %s - %s' % (
            self.cola,
            self.numero,
            self.cliente
        )
