from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from inventory.models import Branch # <-- NUEVO: Importamos Branch desde la app inventory

# Roles definidos en el PDF
class UserRole(models.TextChoices):
    SUPER_ADMIN = 'SUPER_ADMIN', 'Super Admin'
    ADMIN_CLIENTE = 'ADMIN_CLIENTE', 'Admin Cliente'
    GERENTE = 'GERENTE', 'Gerente'
    VENDEDOR = 'VENDEDOR', 'Vendedor'
    CLIENTE_FINAL = 'CLIENTE_FINAL', 'Cliente Final'

class Company(models.Model):
    name = models.CharField(max_length=100)
    rut = models.CharField(max_length=20, unique=True) # Validaremos RUT después
    address = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    # Gestión de Suscripción
    class Plan(models.TextChoices):
        BASIC = 'BASIC', 'Básico'
        STANDARD = 'STANDARD', 'Estándar'
        PREMIUM = 'PREMIUM', 'Premium'

    plan_name = models.CharField(max_length=20, choices=Plan.choices, default=Plan.BASIC)
    subscription_start = models.DateField(default=timezone.now)
    subscription_end = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # Campos solicitados explícitamente 
    rut = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=20, choices=UserRole.choices, default=UserRole.CLIENTE_FINAL)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    
    # NUEVO CAMPO NECESARIO: Relación con la sucursal del vendedor
    branch = models.ForeignKey(Branch, on_delete=models.SET_NULL, null=True, blank=True, related_name='sellers') 
    
    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"