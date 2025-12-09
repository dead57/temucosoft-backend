from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

# Router para las Vistas API
router = DefaultRouter()
router.register(r'sales', views.SaleViewSet)
router.register(r'orders', views.OrderViewSet)

urlpatterns = [
    # 1. RUTA PARA RENDERIZAR LA PÁGINA HTML DEL POS (Paso 1)
    path('pos/', views.pos_page, name='pos_page'), 
    
    # 2. Rutas para las APIs de REST Framework
    path('api/', include(router.urls)),
    path('api/reports/sales/', views.SalesReportView.as_view(), name='sales_report'),
]