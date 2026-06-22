from django.db import migrations


def create_default_roles(apps, schema_editor):
    Rol = apps.get_model('usuarios', 'Rol')
    for nombre, descripcion in (
        ('ADMIN', 'Usuario administrador con acceso total'),
        ('EMPLEADO', 'Usuario operativo con acceso solo a ventas'),
    ):
        Rol.objects.get_or_create(nombre=nombre, defaults={'descripcion': descripcion})


def remove_default_roles(apps, schema_editor):
    Rol = apps.get_model('usuarios', 'Rol')
    Rol.objects.filter(nombre__in=['ADMIN', 'EMPLEADO']).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(create_default_roles, remove_default_roles),
    ]