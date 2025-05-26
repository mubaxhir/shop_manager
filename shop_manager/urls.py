# shop_manager/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from products.views import ProductViewSet, shopify_webhook, update_discount

router = DefaultRouter()
router.register(r'products', ProductViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('webhook/inventory-update/', shopify_webhook),
    path('discount/<int:id>/', update_discount, name='update_discount'),
]
