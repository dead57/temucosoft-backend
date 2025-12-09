from django.db import models
from django.core.validators import MinValueValidator
from django.utils import timezone
from core.models import User, Company
from inventory.models import Branch, Product

# --- SECCIÓN POS (Punto de Venta) ---

class Sale(models.Model):
    PAYMENT_CHOICES = [
        ('CASH', 'Efectivo'),
        ('DEBIT', 'Débito'),
        ('CREDIT', 'Crédito'),
        ('TRANSFER', 'Transferencia'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='sales')
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='sales')
    seller = models.ForeignKey(User, on_delete=models.PROTECT, related_name='sales_made')
    
    payment_method = models.CharField(max_length=20, choices=PAYMENT_CHOICES, default='CASH')
    total = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    
    # Validaremos que no sea fecha futura
    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Venta #{self.id} - {self.branch.name}"

class SaleItem(models.Model):
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.IntegerField(validators=[MinValueValidator(0)]) 
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.price
        super().save(*args, **kwargs)

# --- SECCIÓN E-COMMERCE (Pedidos Web) ---

class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pendiente'),
        ('PAID', 'Pagado'),
        ('SHIPPED', 'Enviado'),
        ('DELIVERED', 'Entregado'),
        ('CANCELLED', 'Anulado'),
    ]

    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='orders')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    
    # Datos cliente invitado
    guest_name = models.CharField(max_length=100, blank=True)
    guest_email = models.EmailField(blank=True)
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total = models.IntegerField(validators=[MinValueValidator(0)], default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Orden #{self.id} - {self.get_status_display()}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.IntegerField(validators=[MinValueValidator(1)])
    price = models.IntegerField(validators=[MinValueValidator(0)])