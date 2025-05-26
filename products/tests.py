from django.urls import reverse
from django.test import TestCase, Client
from .models import Product

class ProductAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name='API Test', sku='skuapi', price=20, inventory_quantity=10)

    def test_product_list_api(self):
        url = '/api/products/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_detail_api(self):
        url = f'/api/products/{self.product.id}/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_product_create_api(self):
        url = '/api/products/'
        data = {'name': 'Created', 'sku': 'skucreated', 'price': 15, 'inventory_quantity': 7}
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [200, 201])

    def test_product_filter_api(self):
        url = '/api/products/?sku=skuapi'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

class WebhookHandlingTests(TestCase):
    def setUp(self):
        self.client = Client()

    def test_webhook_endpoint(self):
        url = '/webhook/inventory-update/'
        payload = {'event': 'product.updated', 'data': {'id': 1}}
        response = self.client.post(url, payload, content_type='application/json')
        self.assertIn(response.status_code, [200, 204])

class DiscountAPITests(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name='Discount Test', sku='skudisc', price=30, inventory_quantity=5)

    def test_discount_api(self):
        url = f'/discount/{self.product.id}/'
        data = {'discount': 10}
        response = self.client.post(url, data)
        self.assertIn(response.status_code, [200, 201])