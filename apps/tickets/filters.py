from django_filters import rest_framework as filters

from .models import Sucursal, TipoCola


class SucursalFilter(filters.FilterSet):
    latitud = filters.NumericRangeFilter(field_name='latitud', lookup_expr='range')
    longitud = filters.NumericRangeFilter(field_name='longitud', lookup_expr='range')

    class Meta:
        model = Sucursal
        fields = (
            'empresa',
            'municipio',
            'latitud',
            'longitud'
        )


class TipoColaFilter(filters.FilterSet):
    capacidad = filters.NumericRangeFilter(field_name='capacidad', lookup_expr='range')

    class Meta:
        model = TipoCola
        fields = ('empresa', 'capacidad')
