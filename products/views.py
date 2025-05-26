# products/views.py
from rest_framework import viewsets, filters
from .models import Product
from .serializers import ProductSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import permissions
from django.db import transaction


@api_view(['POST'])
def shopify_webhook(request):
    payload = request.data

    with transaction.atomic():
        try:
            product = Product.objects.get(sku=payload.get('sku'))
            product.inventory_quantity = payload.get('inventory_quantity')
            product.save()
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)
    return Response({'status': 'updated'}, status=200)
   

class IsInProductManagersGroup(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user and
            request.user.is_authenticated and
            getattr(request.user, 'user_type', None) == 'manager'
        )


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().only(
        'id', 'name', 'sku', 'price', 'inventory_quantity', 'last_updated'
    ).order_by('-last_updated')

    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'sku']
    filterset_fields = ['id','price', 'sku', 'name', 'inventory_quantity']
    ordering_fields = ['id','price', 'inventory_quantity', 'last_updated']


@api_view(['POST'])
def update_discount(request, id):
    percent = float(request.data.get('percent'))
    try:
        product = Product.objects.get(id=id)
        product.price *= (1 - percent / 100)
        product.save()
        return Response({'status': 'discount applied'})
    except Product.DoesNotExist:
        return Response({'error': 'Product not found'}, status=404)
