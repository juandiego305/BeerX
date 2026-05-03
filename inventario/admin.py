from django.contrib import admin
from .models import Categoria, Producto, MovimientosInventario

admin.site.register(Categoria)
admin.site.register(Producto)
admin.site.register(MovimientosInventario)