from django.urls import path, include
from rest_framework import routers

from .views import *

app_name = 'tickets'

router = routers.DefaultRouter()
router.register(r'colas', ColaViewSet)
router.register(r'grupos', GroupViewSet)
router.register(r'tickets', TicketViewSet)
router.register(r'usuarios', UsuarioViewSet)
router.register(r'empresas', EmpresaViewSet)
router.register(r'horarios', HorarioViewSet)
router.register(r'municipios', MunicipioViewSet)
router.register(r'tipos-cola', TipoColaViewSet)
router.register(r'sucursales', SucursalViewSet)
router.register(r'departamentos', DepartamentoViewSet)
router.register(r'tipos-empresa', TipoEmpresaViewSet)
