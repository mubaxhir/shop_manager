# products/views.py
from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response

@api_view(['POST'])
def shopify_webhook(request):
    data = request.data
    sku = data.get('sku')
    quantity = data.get('inventory_quantity')

    try:
        product = Product.objects.get(sku=sku)
        product.inventory_quantity = quantity
        product.save()
        return Response({'status': 'updated'}, status=200)
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().order_by('-last_updated')
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sku']
    ordering_fields = ['price', 'inventory_quantity']


@api_view(['POST'])
def update_discount(request, sku):
    percent = float(request.data.get('percent'))
    try:
        product = Product.objects.get(sku=sku)
        product.price *= (1 - percent / 100)
        product.save()
        return Response({'status': 'discount applied'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
