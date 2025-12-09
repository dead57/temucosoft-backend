from rest_framework import serializers
from django.db import transaction
from .models import Sale, SaleItem, Order, OrderItem
from inventory.models import Inventory

# --- SERIALIZADORES PARA VENTA POS ---

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    
    class Meta:
        model = SaleItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price')
        read_only_fields = ('price',) 

class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True) 
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Sale
        fields = ('id', 'company', 'branch', 'seller', 'seller_name', 'items', 'total', 'payment_method', 'created_at')
        read_only_fields = ('total', 'created_at', 'company', 'seller') 

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        with transaction.atomic():
            sale = Sale.objects.create(**validated_data)
            total_amount = 0

            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                branch = sale.branch

                # Lógica de descuento de stock POS
                try:
                    inventory = Inventory.objects.get(branch=branch, product=product)
                    if inventory.stock < quantity:
                        raise serializers.ValidationError(f"Sin stock de {product.name}")
                    inventory.stock -= quantity
                    inventory.save()
                except Inventory.DoesNotExist:
                    raise serializers.ValidationError(f"Producto {product.name} sin inventario")

                price = product.price
                total_amount += price * quantity
                SaleItem.objects.create(sale=sale, product=product, quantity=quantity, price=price)

            sale.total = total_amount
            sale.save()
            
        return sale

# --- SERIALIZADORES PARA E-COMMERCE ---

class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    class Meta:
        model = OrderItem
        fields = ('id', 'product', 'product_name', 'quantity', 'price')
        
        # --- CORRECCIÓN AQUÍ ---
        # Agregamos esto para que no pida el precio al navegador
        read_only_fields = ('price',) 

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = '__all__'
        read_only_fields = ('total', 'created_at', 'status', 'company')

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        
        # Asignar empresa automáticamente
        from core.models import Company
        company = Company.objects.first() 
        if not company:
            raise serializers.ValidationError("No hay ninguna empresa registrada en el sistema.")
            
        validated_data['company'] = company

        order = Order.objects.create(**validated_data)
        total_amount = 0

        for item_data in items_data:
            product = item_data['product']
            quantity = item_data['quantity']
            price = product.price # El servidor busca el precio real
            
            total_amount += price * quantity
            OrderItem.objects.create(order=order, product=product, quantity=quantity, price=price)

        order.total = total_amount
        order.save()
        return order