from django.contrib import admin

from rest_framework.authtoken.admin import TokenAdmin

from .models import *

TokenAdmin.raw_id_fields = ['user']

admin.site.site_header = 'Ticket Queue App panel de administración'
admin.site.site_title = 'TicketQueueApp - Sitio administrativo'


@admin.register(Usuario)
class UsuarioAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'rol']
    list_display_links = ['username']
    fieldsets = (
        ('Datos personales', {
            'fields': (
                'username',
                'first_name',
                'last_name'
            )
        }),
        ('Datos de contacto', {
            'fields': (
                'email',
                'telefono'
            )
        }),
        ('Otros datos', {
            'fields': (
                'password',
                'rol',
                'sucursal',
                'date_joined',
                'last_login'
            )
        })
    )
    readonly_fields = ['id', 'date_joined', 'last_login']


@admin.register(Departamento)
class DepartamentoAdmin(admin.ModelAdmin):
    list_display = ['nombre']
    list_display_links = ['nombre']
    fieldsets = (
        ('Datos del departamento', {
            'fields': (
                'nombre',
            ),
        }),
    )
    readonly_fields = ['id']


@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
    list_display = ['departamento', 'nombre']
    list_display_links = ['nombre']
    fieldsets = (
        ('Datos del municipio', {
            'fields': (
                'departamento',
                'nombre'
            ),
        }),
    )
    readonly_fields = ['id']


@admin.register(TipoEmpresa)
class TipoEmpresaAdmin(admin.ModelAdmin):
    list_display = ['tipo',]
    list_display_links = ['tipo']
    fieldsets = (
        ('Datos del tipo de empresa', {
            'fields': (
                'tipo',
            ),
        }),
    )
    readonly_fields = ['id']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre','tipo', 'administrador']
    list_display_links = ['nombre']
    fieldsets = (
        ('Datos de la empresa', {
            'fields': (
                'tipo',
                'nombre',
                'nombre_corto',
                'nit',
                'administrador'
            ),
        }),
    )
    readonly_fields = ['id']


@admin.register(TipoCola)
class TipoColaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'capacidad',]
    list_display_links = ['__str__']
    fieldsets = (
        ('Datos del tipo de cola', {
            'fields': (
                'empresa',
                'tipo',
                'descripcion',
                'capacidad'
            ),
        }),
    )
    readonly_fields = ['id']
    

@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'empresa', 'municipio']
    list_display_links = ['nombre']
    fieldsets = (
        ('Datos generales', {
            'fields': (
                'empresa',
                'nombre'
            ),
        }),
        ('Datos de ubicación', {
            'fields': (
                'municipio',
                'direccion',
                'latitud',
                'longitud'
            )
        })
    )
    readonly_fields = ['id']


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'sucursal']
    list_display_links = ['__str__']
    fieldsets = (
        ('Datos del horario', {
            'fields': (
                'sucursal',
                'dia',
                'hora_apertura',
                'hora_cierre'
            ),
        }),
    )
    readonly_fields = ['id']


@admin.register(Cola)
class ColaAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'fecha']
    list_display_links = ['__str__']
    fieldsets = (
        ('Datos de la cola', {
            'fields': (
                'sucursal',
                'tipo_cola',
                'horario',
                'fecha'
            ),
        }),
    )
    readonly_fields = ['id']
    

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'estado', 'hora_generado', 'cajero']
    list_display_links = ['__str__']
    fieldsets = (
        ('Datos del ticket', {
            'fields': (
                'cola',
                'cliente',
                'numero',
                'hora_generado',
                'estado',
                'cant_intentos',
                'cajero'
            ),
        }),
    )
    readonly_fields = ['hora_generado', 'id']
