# products/tests.py
from django.test import TestCase
from .models import Product

class ProductModelTest(TestCase):
    def test_create_product(self):
        product = Product.objects.create(name='Test', sku='123', price=10, inventory_quantity=5)
        self.assertEqual(product.name, 'Test')
