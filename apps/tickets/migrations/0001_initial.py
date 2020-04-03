# Generated by Django 3.0.5 on 2020-04-02 20:48

from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('telefono', phonenumber_field.modelfields.PhoneNumberField(blank=True, default=None, help_text='Ingrese su número de teléfono en el formato +41524204242', max_length=128, null=True, region=None, verbose_name='número de teléfono')),
                ('rol', models.PositiveSmallIntegerField(choices=[(1, 'CAJERO'), (2, 'USUARIO'), (3, 'ADMINISTRADOR')], default=2, help_text='Seleccione el ROL del usuario.', validators=[django.core.validators.MinValueValidator(1, 'La opción seleccionada es inválida'), django.core.validators.MaxValueValidator(3, 'La opción seleccionada es inválida')], verbose_name='rol')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'usuario',
                'verbose_name_plural': 'usuarios',
                'ordering': ['rol', 'username'],
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Cola',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField(auto_now_add=True, help_text='Fecha en la que se habilitará esta cola.', verbose_name='fecha')),
            ],
            options={
                'verbose_name': 'cola',
                'verbose_name_plural': 'colas',
                'ordering': ['fecha', 'sucursal', 'horario', 'tipo_cola'],
            },
        ),
        migrations.CreateModel(
            name='Departamento',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ingrese el nombre de este departamento.', max_length=50, verbose_name='nombre')),
            ],
            options={
                'verbose_name': 'departamento',
                'verbose_name_plural': 'departamentos',
                'ordering': ['nombre'],
            },
        ),
        migrations.CreateModel(
            name='Empresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ingrese el nombre de la empresa.', max_length=150, verbose_name='nombre')),
                ('nombre_corto', models.CharField(help_text='Ingrese el nombre corto de la empresa.', max_length=50, verbose_name='nombre corto')),
                ('nit', models.CharField(help_text='Ingrese el NIT de la empresa.', max_length=17, verbose_name='nit')),
                ('administrador', models.ForeignKey(blank=True, default=None, help_text='Seleccione el administrador del sistema para esta empresa.', null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='administrador')),
            ],
            options={
                'verbose_name': 'empresa',
                'verbose_name_plural': 'empresas',
                'ordering': ['nombre', 'nombre_corto'],
            },
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ingrese el nombre de este municipio.', max_length=50, verbose_name='nombre')),
                ('departamento', models.ForeignKey(help_text='Seleccione el departamento', on_delete=django.db.models.deletion.CASCADE, to='tickets.Departamento', verbose_name='departamento')),
            ],
            options={
                'verbose_name': 'municipio',
                'verbose_name_plural': 'municipios',
                'ordering': ['departamento', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='TipoEmpresa',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(help_text='Ingrese el tipo de empresa.', max_length=30, verbose_name='tipo')),
            ],
            options={
                'verbose_name': 'tipo de empresa',
                'verbose_name_plural': 'tipos de empresa',
                'ordering': ['tipo'],
            },
        ),
        migrations.CreateModel(
            name='TipoCola',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(help_text='Ingrese el nombre de este tipo de cola.', max_length=30, verbose_name='tipo de cola')),
                ('descripcion', models.CharField(blank=True, default=None, help_text='Ingrese una descripción.', max_length=150, null=True, verbose_name='descripcion')),
                ('capacidad', models.PositiveSmallIntegerField(help_text='Ingrese la capacidad máxima de esta cola.', verbose_name='capacidad')),
                ('empresa', models.ForeignKey(help_text='Selecccione la empresa a la que pertenece este tipo de cola.', on_delete=django.db.models.deletion.CASCADE, to='tickets.Empresa', verbose_name='empresa')),
            ],
            options={
                'verbose_name': 'tipo de cola',
                'verbose_name_plural': 'tipos de cola',
                'ordering': ['empresa', 'capacidad', 'tipo'],
            },
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(help_text='Ingrese el número del ticket.', max_length=10, verbose_name='número')),
                ('estado', models.PositiveSmallIntegerField(choices=[(1, 'ESPERA'), (2, 'ACTIVO'), (3, 'PASO'), (4, 'VENCIDO'), (5, 'RETIRADO')], default=1, help_text='Seleccione el estado actual de este ticket.', validators=[django.core.validators.MinValueValidator(1, 'La opción seleccionada es inválida'), django.core.validators.MaxValueValidator(5, 'La opción seleccionada es inválida')], verbose_name='estado')),
                ('hora_generado', models.TimeField(auto_now_add=True, help_text='Hora en la que se generó este ticket.', verbose_name='hora de generación')),
                ('cant_intentos', models.PositiveSmallIntegerField(default=1, help_text='Ingrese la cantidad de intentos que se hizo para despachar este ticket.', validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(3, 'Solo se permiten 3 intentos.')], verbose_name='cantidad de intentos')),
                ('cajero', models.ForeignKey(help_text='Seleccione el cajero que despachó este ticket.', null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cajero', to=settings.AUTH_USER_MODEL, verbose_name='cajero')),
                ('cliente', models.ForeignKey(help_text='Seleccione el usuario al que le asignará este ticket.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='cliente', to=settings.AUTH_USER_MODEL, verbose_name='cliente')),
                ('cola', models.ForeignKey(help_text='Seleccione la cola a la que asignará este ticket.', on_delete=django.db.models.deletion.CASCADE, to='tickets.Cola', verbose_name='cola')),
            ],
        ),
        migrations.CreateModel(
            name='Sucursal',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(help_text='Ingrese el nombre de la empresa.', max_length=150, verbose_name='nombre')),
                ('latitud', models.DecimalField(blank=True, decimal_places=6, help_text='La latitud está dada en grados decimales, entre 0° y 90 ° en el hemisferio Norte y entre 0° y -90° en el hemisferio Sur', max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-90.0), django.core.validators.MaxValueValidator(90.0)], verbose_name='latitud')),
                ('longitud', models.DecimalField(blank=True, decimal_places=6, help_text='La longitud está dada en grados decimales, entre 0° y 180°, al este del meridiano de Greenwich y entre 0° y -180°, al oeste del meridiano de Greenwich.', max_digits=9, null=True, validators=[django.core.validators.MinValueValidator(-180.0), django.core.validators.MaxValueValidator(180.0)], verbose_name='longitud')),
                ('direccion', models.CharField(blank=True, help_text='Ingrese la dirección.', max_length=200, null=True, verbose_name='dirección')),
                ('empresa', models.ForeignKey(help_text='Selecccione la empresa a la que pertenece esta sucursal.', on_delete=django.db.models.deletion.CASCADE, to='tickets.Empresa', verbose_name='empresa')),
                ('municipio', models.ForeignKey(help_text='Seleccione el municipio en el que se encuentra esta sucursal.', on_delete=django.db.models.deletion.CASCADE, to='tickets.Municipio', verbose_name='municipio')),
            ],
            options={
                'verbose_name': 'sucursal',
                'verbose_name_plural': 'sucursales',
                'ordering': ['empresa', 'municipio', 'nombre'],
            },
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('hora_apertura', models.TimeField()),
                ('hora_cierre', models.TimeField()),
                ('dia', models.IntegerField(choices=[(1, 'DOMINGO'), (2, 'LUNES'), (3, 'MARTES'), (4, 'MIÉRCOLES'), (5, 'JUEVES'), (6, 'VIERNES'), (7, 'SÁBADO')], default=2, help_text='Seleccione el día en que se tiene este horario.', validators=[django.core.validators.MinValueValidator(1, 'La opción seleccionada es inválida'), django.core.validators.MaxValueValidator(7, 'La opción seleccionada es inválida')], verbose_name='rol')),
                ('sucursal', models.ForeignKey(help_text='Seleccione una sucursal para este horario.', on_delete=django.db.models.deletion.CASCADE, to='tickets.Sucursal', verbose_name='sucursal')),
            ],
            options={
                'verbose_name': 'horario',
                'verbose_name_plural': 'horarios',
                'ordering': ['sucursal', 'dia', 'hora_apertura', 'hora_cierre'],
            },
        ),
        migrations.AddField(
            model_name='empresa',
            name='tipo',
            field=models.ForeignKey(default=None, help_text='Seleccione el tipo de empresa.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tickets.TipoEmpresa', verbose_name='tipo de empresa'),
        ),
        migrations.AddField(
            model_name='cola',
            name='horario',
            field=models.ForeignKey(help_text='Seleccione el horario en el cual esta cola estará habilitada', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tickets.Horario', verbose_name='horario'),
        ),
        migrations.AddField(
            model_name='cola',
            name='sucursal',
            field=models.ForeignKey(help_text='Seleccione la sucursal para la que habilitará esta cola.', on_delete=django.db.models.deletion.CASCADE, to='tickets.Sucursal', verbose_name='sucursal'),
        ),
        migrations.AddField(
            model_name='cola',
            name='tipo_cola',
            field=models.ForeignKey(help_text='Seleccione el tipo de esta cola.', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='tickets.TipoCola', verbose_name='tipo de cola'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='sucursal',
            field=models.ForeignKey(blank=True, default=None, help_text='Seleccione una sucursal si este usuario tiene el rol "CAJERO".', null=True, on_delete=django.db.models.deletion.CASCADE, to='tickets.Sucursal', verbose_name='sucursal'),
        ),
        migrations.AddField(
            model_name='usuario',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]
