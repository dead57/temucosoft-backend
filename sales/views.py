from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from django.db.models import Sum
from django.db.models.functions import TruncDate
from .models import Sale, Order
from .serializers import SaleSerializer, OrderSerializer

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

# ESTA ES LA CLASE QUE FALTABA Y CAUSABA EL ERROR
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