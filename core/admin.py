from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company
from inventory.models import Branch

# Personalizamos el panel de usuario para que muestre tus campos nuevos
class CustomUserAdmin(UserAdmin):
    # Agregamos una sección nueva en la pantalla de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Datos TemucoSoft', {'fields': ('rut', 'role', 'company', 'branch')}), # <<< BRANCH AÑADIDO AQUI
    )
    
    # Agregamos los campos también a la pantalla de crear usuario
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos TemucoSoft', {'fields': ('rut', 'role', 'company', 'branch')}), # <<< BRANCH AÑADIDO AQUI
    )
    
    # Columnas que se ven en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'role', 'company', 'branch', 'is_staff') # <<< BRANCH AÑADIDO AQUI
    list_filter = ('role', 'company', 'branch', 'is_staff') # <<< BRANCH AÑADIDO AQUI

# Registramos usando nuestra configuración personalizada
admin.site.register(User, CustomUserAdmin)