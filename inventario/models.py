from django.db import models
# Importamos el usuario que creamos en la otra app
from usuarios.models import Usuario

class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'categorias'
        managed = False # Le dice a Django: "La tabla ya existe en Neon, no la toques"
        verbose_name = 'Categoría'
        verbose_name_plural = 'Categorías'

    def __str__(self):
        return self.nombre

class Producto(models.Model):
    # Relación con la categoría
    categoria = models.ForeignKey(Categoria, on_delete=models.RESTRICT)
    sku = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=150)
    unidad_medida = models.CharField(max_length=20)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2, default=10.00)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'productos'
        managed = False

    def __str__(self):
        return self.nombre

class MovimientosInventario(models.Model):
    TIPO_CHOICES = [
        ('ENTRADA', 'Entrada'),
        ('SALIDA', 'Salida'),
        ('MERMA', 'Merma'),
    ]
    
    producto = models.ForeignKey(Producto, on_delete=models.RESTRICT)
    usuario = models.ForeignKey(Usuario, on_delete=models.RESTRICT)
    tipo_movimiento = models.CharField(max_length=20, choices=TIPO_CHOICES)
    cantidad = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_movimiento = models.DateTimeField(auto_now_add=True)
    observaciones = models.TextField(blank=True, null=True)

    class Meta:
        db_table = 'movimientos_inventario'
        managed = False
        verbose_name = 'Movimiento de Inventario'
        verbose_name_plural = 'Movimientos de Inventario'

    def __str__(self):
        return f"{self.tipo_movimiento} - {self.producto.nombre} ({self.cantidad})"
    
class StockActual(models.Model):
    producto_id = models.IntegerField(primary_key=True)
    sku = models.CharField(max_length=50)
    producto = models.CharField(max_length=150)
    categoria = models.CharField(max_length=100)
    unidad_medida = models.CharField(max_length=20)
    stock_minimo = models.DecimalField(max_digits=10, decimal_places=2)
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)
    stock_total = models.DecimalField(max_digits=10, decimal_places=2)
    alerta_stock = models.BooleanField()

    class Meta:
        managed = False  # Django no intentará crear ni modificar esta tabla
        db_table = 'vw_stock_actual' # El nombre exacto de la vista en Neon