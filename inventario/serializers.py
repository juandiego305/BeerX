from rest_framework import serializers
from inventario.models import Categoria, Producto, MovimientosInventario, StockActual

class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = '__all__'
    
# Asegúrate de importar StockActual arriba junto a los otros modelos:
# from inventario.models import Categoria, Producto, MovimientosInventario, StockActual

class StockActualSerializer(serializers.ModelSerializer):
    class Meta:
        model = StockActual
        fields = '__all__'

class ProductoSerializer(serializers.ModelSerializer):
    # Este campo extra es un truco para que el frontend reciba el nombre 
    # de la categoría directamente, y no solo un ID numérico aburrido.
    categoria_nombre = serializers.ReadOnlyField(source='categoria.nombre')

    class Meta:
        model = Producto
        fields = '__all__'

class MovimientoSerializer(serializers.ModelSerializer):
    # El usuario ahora es automático, no se pide en el JSON
    usuario = serializers.ReadOnlyField(source='usuario.username')

    class Meta:
        model = MovimientosInventario
        fields = '__all__'

    def validate(self, data):
        """
        Validación a nivel de objeto para el stock.
        """
        tipo = data.get('tipo_movimiento')
        cantidad_solicitada = data.get('cantidad')
        producto = data.get('producto')
        request = self.context.get('request')
        usuario = getattr(request, 'user', None)
        es_admin = bool(usuario and usuario.is_authenticated and usuario.rol and usuario.rol.nombre.upper() == 'ADMIN')

        if not es_admin and tipo != 'SALIDA':
            raise serializers.ValidationError({
                'tipo_movimiento': 'El usuario empleado solo puede registrar ventas tipo SALIDA.'
            })

        if tipo == 'SALIDA':
            # Consultamos la vista de stock actual en Neon
            estado_stock = StockActual.objects.filter(producto_id=producto.id).first()
            stock_disponible = estado_stock.stock_total if estado_stock else 0

            if cantidad_solicitada > stock_disponible:
                raise serializers.ValidationError({
                    "cantidad": f"No hay suficiente stock. Disponible: {stock_disponible}, Solicitado: {cantidad_solicitada}"
                })
        
        return data

    def create(self, validated_data):
        # Asignamos el usuario que está haciendo la petición desde el token
        validated_data['usuario'] = self.context['request'].user
        return super().create(validated_data)

