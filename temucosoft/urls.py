from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Importamos las vistas de nuestras apps
from core.views import UserViewSet, CompanyViewSet
from inventory.views import ProductViewSet, BranchViewSet, SupplierViewSet, InventoryViewSet, StockReportView
from sales.views import SaleViewSet, OrderViewSet, SalesReportView

# --- CONFIGURACIÓN DEL ROUTER API ---
router = DefaultRouter()
# Rutas de Core
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
# Rutas de Inventario
router.register(r'products', ProductViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'inventory', InventoryViewSet, basename='inventory')
# Rutas de Ventas
router.register(r'sales', SaleViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    # 1. Panel de Administración Django
    path('admin/', admin.site.urls),

    # 2. Rutas de la API (CRUDs automáticos)
    path('api/', include(router.urls)),

    # 3. Autenticación JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # 4. Endpoints de Reportes (Manuales)
    path('api/reports/sales/', SalesReportView.as_view(), name='report-sales'),
    path('api/reports/stock/', StockReportView.as_view(), name='report-stock'),

    # 5. Documentación de API (Swagger / Spectacular)
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    # 6. Frontend (Páginas HTML)
    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('pos/', TemplateView.as_view(template_name='pos.html'), name='pos'),
    path('reports/', TemplateView.as_view(template_name='reports.html'), name='reports'),
    path('shop/', TemplateView.as_view(template_name='catalog.html'), name='shop'),
]

# Configuración para servir imágenes (MEDIA) en modo DEBUG
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)