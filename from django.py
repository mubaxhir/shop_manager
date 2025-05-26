from django.urls import reverse
from django.test import TestCase, Client
from .tests import ProductModelTest
from .models import Product

class ProductModelTestTests(TestCase):
    def test_create_product(self):
        test_case = ProductModelTest()
        test_case.setUpClass()
        try:
            test_case.test_create_product()
        finally:
            test_case.tearDownClass()

class ProductAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name='API Test', sku='skuapi', price=20, inventory_quantity=10)

    def test_product_list_api(self):
        url = reverse('product-list')  # Assumes you have a url named 'product-list'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_api(self):
        url = reverse('product-detail', args=[self.product.id])  # Assumes you have a url named 'product-detail'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_create_api(self):
        url = reverse('product-list')
        data = {'name': 'Created', 'sku': 'skucreated', 'price': 15, 'inventory_quantity': 7}
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [200, 201])

class WebhookHandlingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webhook_endpoint(self):
        url = reverse('webhook-endpoint')  # Assumes you have a url named 'webhook-endpoint'
        payload = {'event': 'product.updated', 'data': {'id': 1}}
        response = self.client.post(url, payload, content_type='application/json')
        self.assertIn(response.status_code, [200, 204])