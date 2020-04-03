from rest_framework import permissions


from .models import *

def is_authenticated(request):
    return request.user and request.user.is_authenticated


class ReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS


class IsOwner(permissions.BasePermission):

    def has_permission(self, request, view):
        try:
            user = Usuario.objects.get(pk=view.kwargs['pk'])
        except:
            return False
        return request.user == user


class IsSuperUser(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return is_authenticated(request) and request.user.is_superuser


class IsAdministrador(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return is_authenticated(request) and request.user.rol == Rol.ADMINISTRADOR
    
    def has_object_permission(self, request, view, obj):
        is_administrador = False
        if is_authenticated(request):
            if request.user.rol == Rol.ADMINISTRADOR:
                if isinstance(obj, Empresa):
                    is_administrador = obj.administrador == request.user
                elif isinstance(obj, Sucursal, TipoCola):
                    is_administrador = obj.empresa.administrador == request.user
                elif isinstance(obj, Horario, Cola, Usuario):
                    is_administrador = obj.sucursal.empresa.administrador == request.user
                elif isinstance(obj, Ticket):
                    is_administrador = obj.cola.sucursal.empresa.administrador == request.user
        print(is_administrador)
        return is_administrador


class IsCajero(permissions.BasePermission):
    
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        return is_authenticated(request) and request.user.rol == Rol.CAJERO
    
    def has_object_permission(self, request, view, obj):
        is_cajero = False
        if is_authenticated(request):
            if request.user.rol == Rol.CAJERO:
                if isinstance(obj, Horario, Cola):
                    is_cajero = obj.sucursal == request.user.sucursal
                elif isinstance(obj, Ticket):
                    is_cajero = obj.cola.sucursal == request.user.sucursal
        return is_cajero


class IsUsuario(permissions.BasePermission):
    
    def has_permission(self, request, view):
        return is_authenticated(request) and request.user.rol == Rol.USUARIO
    
    def has_object_permission(self, request, view, obj):
        return (
            is_authenticated(request) and
            request.user.rol == Rol.USUARIO and
            obj.cliente == request.user.sucursal
        )


