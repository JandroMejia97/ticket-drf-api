from django.core import exceptions
from django.contrib.auth import password_validation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group

from rest_framework import serializers, validators as drf_validators

from apps.core.serializers import DynamicFieldsModelSerializer

from .models import *


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        model = Group
        fields = ('__all__')


class UsuarioSerializer(DynamicFieldsModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[drf_validators.UniqueValidator(queryset=Usuario.objects.all())]
    )
    is_active = serializers.BooleanField(
        default=True,
        label='Es activo',
        help_text='Indica si el usuario debe ser tratado como activo. Desmarque esta opción en lugar de borrar la cuenta.'
    )

    class Meta:
        model = Usuario
        exclude = ('groups', 'user_permissions')
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def update(self, instance, validated_data):
        fields = instance._meta.fields
        for field in fields:
            field = field.name.split('.')[-1]
            exec("instance.%s = validated_data.get(field, instance.%s)" % (field, field))
        instance.password = make_password(validated_data.get('password', instance.password))
        
        instance.save()
        return instance
    
    def create(self, validated_data):
        username = validated_data.pop('username')
        password = validated_data.pop('password')
        email = validated_data.pop('email')
        user = Usuario.objects.create_user(
            username=username,
            email=email,
            password=password,
            **validated_data
        )
        return user

    def validate(self, data):
        user = Usuario(**data)
        password = data.get('password')
        errors = dict() 
        try:
            password_validation.validate_password(password=password, user=user)

        except exceptions.ValidationError as e:
            errors['password'] = list(e.messages)

        if errors:
            raise serializers.ValidationError(errors)
        return super(UsuarioSerializer, self).validate(data)


class DepartamentoSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Departamento
        fields = ('__all__')


class MunicipioSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Municipio
        fields = ('__all__')


class TipoEmpresaSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = TipoEmpresa
        fields = ('__all__')


class EmpresaSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Empresa
        fields = ('__all__')


class TipoColaSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = TipoCola
        fields = ('__all__')


class SucursalSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Sucursal
        fields = ('__all__')


class HorarioSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Horario
        fields = ('__all__')


class ColaSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Cola
        fields = ('__all__')

class TicketSerializer(DynamicFieldsModelSerializer):

    class Meta:
        model = Ticket
        fields = ('__all__')
