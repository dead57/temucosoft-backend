from rest_framework import viewsets, permissions
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Product, Branch, Supplier, Inventory, Category
from .serializers import ProductSerializer, BranchSerializer, SupplierSerializer, InventorySerializer, CategorySerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    # --- CAMBIO IMPORTANTE PARA E-COMMERCE ---
    # Permitimos que cualquiera vea (GET), pero solo usuarios logueados editen.
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

class BranchViewSet(viewsets.ModelViewSet):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [permissions.IsAuthenticated]

class SupplierViewSet(viewsets.ModelViewSet):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = [permissions.IsAuthenticated]

class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Permite filtrar inventario por sucursal: /api/inventory/?branch=1
        queryset = Inventory.objects.all()
        branch_id = self.request.query_params.get('branch', None)
        if branch_id is not None:
            queryset = queryset.filter(branch_id=branch_id)
        return queryset

class StockReportView(APIView):
    """
    Endpoint para reporte de stock general (Usado en Dashboard -> Reportes)
    """
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        inventory = Inventory.objects.all().select_related('product', 'branch')
        data = []
        for item in inventory:
            data.append({
                'branch': item.branch.name,
                'product': item.product.name,
                'sku': item.product.sku,
                'stock': item.stock,
                'price': item.product.price
            })
        return Response(data)