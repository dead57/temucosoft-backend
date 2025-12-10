from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic import TemplateView
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

# Importamos las vistas
from core.views import UserViewSet, CompanyViewSet
from inventory.views import ProductViewSet, BranchViewSet, SupplierViewSet, InventoryViewSet, StockReportView
# 👇 AQUÍ AGREGAMOS 'pos_page'
from sales.views import SaleViewSet, OrderViewSet, SalesReportView, pos_page

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'companies', CompanyViewSet)
router.register(r'products', ProductViewSet)
router.register(r'branches', BranchViewSet)
router.register(r'suppliers', SupplierViewSet)
router.register(r'inventory', InventoryViewSet, basename='inventory')
router.register(r'sales', SaleViewSet)
router.register(r'orders', OrderViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/reports/sales/', SalesReportView.as_view(), name='report-sales'),
    path('api/reports/stock/', StockReportView.as_view(), name='report-stock'),
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),

    path('login/', TemplateView.as_view(template_name='login.html'), name='login'),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    
    # 👇 ESTA ES LA CORRECCIÓN CRUCIAL: Usamos tu vista Python real
    path('pos/', pos_page, name='pos'),
    
    path('reports/', TemplateView.as_view(template_name='reports.html'), name='reports'),
    path('shop/', TemplateView.as_view(template_name='catalog.html'), name='shop'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)