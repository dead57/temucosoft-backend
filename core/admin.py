from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Company # <-- Importamos Company para registrarlo.

# Personalizamos el panel de usuario
class CustomUserAdmin(UserAdmin):
    # Agregamos los campos a la sección de edición
    fieldsets = UserAdmin.fieldsets + (
        ('Datos TemucoSoft', {'fields': ('rut', 'role', 'company', 'branch')}), 
    )
    
    # Agregamos los campos a la sección de creación de usuarios
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Datos TemucoSoft', {'fields': ('rut', 'role', 'company', 'branch')}),
    )
    
    # Columnas que se ven en la lista de usuarios
    list_display = ('username', 'email', 'first_name', 'role', 'company', 'branch', 'is_staff')
    list_filter = ('role', 'company', 'branch', 'is_staff')

# 1. Registramos el modelo de Usuario con nuestra personalización
admin.site.register(User, CustomUserAdmin)

# 2. REGISTRAMOS EL MODELO DE COMPAÑÍA para que aparezca en el Admin.
admin.site.register(Company)