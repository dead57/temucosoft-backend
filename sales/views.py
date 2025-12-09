from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncDate
from django.shortcuts import render # <-- NUEVA IMPORTACIÓN
from django.contrib.auth.decorators import login_required # <-- NUEVA IMPORTACIÓN

from .models import Sale, Order
from .serializers import SaleSerializer, OrderSerializer

# --- VISTAS API EXISTENTES ---
class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Asigna automáticamente el usuario que vende y su empresa
        serializer.save(seller=self.request.user, company=self.request.user.company)

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.AllowAny] 

class SalesReportView(APIView):
    """
    Endpoint para reporte de ventas diarias.
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        sales_data = Sale.objects.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            total_sales=Sum('total')
        ).order_by('-date')

        return Response(sales_data)

# --- VISTA DE RENDERIZADO DEL POS (NUEVO CÓDIGO) ---
@login_required
def pos_page(request):
    """
    Renderiza la plantilla del POS. 
    Pasa la sucursal asignada al usuario logueado para que el Frontend filtre el inventario.
    """
    current_branch = request.user.branch
    
    # Creamos el contexto con la información de la sucursal
    context = {
        # Esta variable se usará en el HTML/JS para mostrar el nombre
        'current_branch_name': current_branch.name if current_branch else 'Sucursal Default',
        # Esta variable puede usarse en JS para filtrar la API de inventario
        'current_branch_id': current_branch.id if current_branch else None,
    }
    
    # El nombre de la plantilla debe coincidir con tu archivo HTML del POS
    return render(request, 'pos_page.html', context)