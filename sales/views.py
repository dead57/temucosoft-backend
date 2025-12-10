from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncDate
# --- IMPORTACIONES NUEVAS NECESARIAS ---
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .models import Sale, Order
from .serializers import SaleSerializer, OrderSerializer

# --- TUS VISTAS API (Se mantienen igual) ---

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
    Devuelve: [{date: '2025-12-09', total_sales: 2500}, ...]
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Agrupamos las ventas por Fecha (día) y sumamos el total
        sales_data = Sale.objects.annotate(
            date=TruncDate('created_at')
        ).values('date').annotate(
            total_sales=Sum('total')
        ).order_by('-date')

        return Response(sales_data)

# --- VISTA NUEVA PARA RENDERIZAR EL POS (HTML) ---
@login_required
def pos_page(request):
    """
    Renderiza la plantilla HTML del POS y pasa el contexto de la sucursal.
    """
    # 🚨 DEBUGGING: Esto imprimirá en la terminal de AWS los datos reales
    print(f"DEBUG: Usuario logueado: {request.user.username}")
    
    try:
        # Intentamos imprimir el ID y el objeto para ver si existen
        print(f"DEBUG: Valor de Branch ID: {request.user.branch_id}")
        print(f"DEBUG: Objeto Branch completo: {request.user.branch}")
    except Exception as e:
        print(f"DEBUG: Error al intentar leer la sucursal: {e}")

    current_branch = request.user.branch
    
    # Creamos el contexto con la información de la sucursal para usar en el Template
    context = {
        'current_branch_name': current_branch.name if current_branch else 'Error: Sucursal no asignada',
        'current_branch_id': current_branch.id if current_branch else None,
    }
    
    # NOTA: Asegúrate de que tu archivo en la carpeta 'templates' se llame 'pos.html'
    # Si se llama 'pos_page.html', cambia el nombre aquí abajo.
    return render(request, 'pos.html', context)