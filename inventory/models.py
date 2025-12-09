from django.db import models
from django.core.validators import MinValueValidator
from core.models import Company

# 1. Proveedores
class Supplier(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre Proveedor")
    rut = models.CharField(max_length=20, verbose_name="RUT") 
    contact = models.CharField(max_length=100, verbose_name="Contacto (Email/Tel)")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='suppliers')
    
    def __str__(self):
        return f"{self.name} ({self.rut})"

# 2. Sucursales
class Branch(models.Model):
    name = models.CharField(max_length=100, verbose_name="Nombre Sucursal")
    address = models.CharField(max_length=255, verbose_name="Dirección")
    phone = models.CharField(max_length=20, verbose_name="Teléfono")
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='branches')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Sucursal"
        verbose_name_plural = "Sucursales"

# 3. Categoría
class Category(models.Model):
    name = models.CharField(max_length=50)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='categories')
    
    def __str__(self):
        return self.name

# 4. Productos
class Product(models.Model):
    sku = models.CharField(max_length=50, verbose_name="SKU")
    name = models.CharField(max_length=100, verbose_name="Nombre")
    description = models.TextField(blank=True, verbose_name="Descripción")
    image = models.ImageField(upload_to='products/', null=True, blank=True, verbose_name="Imagen Producto")
    
    # Validacion PDF: Precio >= 0
    price = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Precio Venta")
    cost = models.IntegerField(validators=[MinValueValidator(0)], verbose_name="Costo")
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='products')
    
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"

    class Meta:
        unique_together = ('company', 'sku')

# 5. Inventario (Relación Sucursal <-> Producto)
class Inventory(models.Model):
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='inventories')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='inventories')
    
    # Validacion PDF: Stock >= 0
    stock = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    reorder_point = models.IntegerField(default=10, verbose_name="Punto de reorden")

    class Meta:
        unique_together = ('branch', 'product')
        verbose_name = "Inventario"
        verbose_name_plural = "Inventarios"

    def __str__(self):
        return f"{self.product.name} en {self.branch.name}: {self.stock}"