from django.shortcuts import render
from django.contrib.auth.models import Group

from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated

from .serializers import *
from .filters import SucursalFilter, TipoColaFilter
from .permissions import (
    IsOwner,
    IsCajero,
    ReadOnly,
    IsUsuario,
    IsSuperUser,
    IsAdministrador,
)


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsSuperUser]


class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    permission_classes = [IsOwner | IsAdministrador | IsSuperUser]
    filterset_fields = (
        'rol',
        'sucursal'
    )


class DepartamentoViewSet(viewsets.ModelViewSet):
    queryset = Departamento.objects.all()
    serializer_class = DepartamentoSerializer
    permission_classes = [ReadOnly | IsSuperUser]


class MunicipioViewSet(viewsets.ModelViewSet):
    queryset = Municipio.objects.all()
    serializer_class = MunicipioSerializer
    permission_classes = [ReadOnly | IsSuperUser]
    filterset_fields = ('departamento',)


class TipoEmpresaViewSet(viewsets.ModelViewSet):
    queryset = TipoEmpresa.objects.all()
    serializer_class = TipoEmpresaSerializer
    permission_classes = [ReadOnly | IsSuperUser]


class EmpresaViewSet(viewsets.ModelViewSet):
    queryset = Empresa.objects.all()
    serializer_class = EmpresaSerializer
    permission_classes = [IsAdministrador | IsSuperUser]
    filterset_fields = ('tipo',)

    def get_queryset(self):
        if self.request.user.rol == Rol.ADMINISTRADOR:
            return Empresa.objects.filter(administrador=self.request.user)
        return super().get_queryset()


class TipoColaViewSet(viewsets.ModelViewSet):
    queryset = TipoCola.objects.all()
    filter_class = TipoColaFilter
    serializer_class = TipoColaSerializer
    permission_classes = [IsAdministrador | IsSuperUser]

    def get_queryset(self):
        if self.request.user.rol == Rol.ADMINISTRADOR:
            return TipoCola.objects.filter(empresa__administrador=self.request.user)
        return super().get_queryset()


class SucursalViewSet(viewsets.ModelViewSet):
    queryset = Sucursal.objects.all()
    serializer_class = SucursalSerializer
    filter_class = SucursalFilter
    permission_classes = [
        ReadOnly |
        IsAdministrador |
        IsSuperUser
    ]

    def get_queryset(self):
        if self.request.user.rol == Rol.ADMINISTRADOR:
            return Sucursal.objects.filter(empresa__administrador=self.request.user)
        if self.request.user.rol == Rol.CAJERO:
            return Sucursal.objects.filter(pk=self.request.user.sucursal.id)
        return super().get_queryset()


class HorarioViewSet(viewsets.ModelViewSet):
    queryset = Horario.objects.all()
    serializer_class = HorarioSerializer
    permission_classes = [
        ReadOnly |
        IsCajero |
        IsAdministrador |
        IsSuperUser
    ]
    filterset_fields = (
        'dia',
        'sucursal',
        'hora_cierre',
        'hora_apertura',
    )

    def get_queryset(self):
        if self.request.user.rol == Rol.ADMINISTRADOR:
            return Horario.objects.filter(
                sucursal__empresa__administrador=self.request.user
            )
        if self.request.user.rol == Rol.CAJERO:
            return Horario.objects.filter(sucursal=self.request.user.sucursal)
        return super().get_queryset()


class ColaViewSet(viewsets.ModelViewSet):
    queryset = Cola.objects.all()
    serializer_class = ColaSerializer
    permission_classes = [
        ReadOnly |
        IsCajero |
        IsAdministrador |
        IsSuperUser
    ]
    filterset_fields = (
        'fecha',
        'tipo_cola',
        'sucursal',
        'sucursal__empresa',
        'tipo_cola__empresa'
    )

    def get_queryset(self):
        if self.request.user.rol == Rol.ADMINISTRADOR:
            return Cola.objects.filter(sucursal__empresa__administrador=self.request.user)
        if self.request.user.rol == Rol.CAJERO:
            return Cola.objects.filter(sucursal=self.request.user.sucursal)
        return super().get_queryset()


class TicketViewSet(viewsets.ModelViewSet):
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [
        ReadOnly |
        IsUsuario |
        IsCajero |
        IsAdministrador |
        IsSuperUser
    ]
    filterset_fields = (
        'cola',
        'estado',
        'cajero',
        'cliente',
        'cola__sucursal',
        'cant_intentos',
        'cajero__sucursal',
    )

    def get_queryset(self):
        if self.request.user.rol == Rol.ADMINISTRADOR:
            return Ticket.objects.filter(
                cola__sucursal__empresa__administrador=self.request.user
            )
        if self.request.user.rol == Rol.CAJERO:
            return Ticket.objects.filter(cola__sucursal=self.request.user.sucursal)
        return super().get_queryset()
