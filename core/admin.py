from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User # <-- Solo necesitamos User aquí
from inventory.models import Branch # <-- Asegúrate de que esta línea esté, si la estás usando
from core.models import Company #

# Personalizamos el panel de usuario para que muestre tus campos nuevos
class CustomUserAdmin(UserAdmin):
    # Agregamos los campos a la sección de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Datos TemucoSoft', {'fields': ('rut', 'role', 'company', 'branch')}), # <<< BRANCH AÑADIDO
    )
    
    # Agregamos los campos a la sección de creación de usuarios
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos TemucoSoft', {'fields': ('rut', 'role', 'company', 'branch')}), # <<< BRANCH AÑADIDO
    )
    
    # Columnas que se ven en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'role', 'company', 'branch', 'is_staff') # <<< BRANCH AÑADIDO
    list_filter = ('role', 'company', 'branch', 'is_staff') # <<< BRANCH AÑADIDO

# Registramos usando nuestra configuración personalizada
admin.site.register(User, CustomUserAdmin)