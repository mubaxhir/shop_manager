# products/tasks.py
from celery import shared_task
import csv
from .models import Product
from django.core.mail import send_mail

@shared_task
def import_csv():
    with open('products.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = list(reader)
        return data

@shared_task
def validate_and_update(data):
    updated = []
    for row in data:
        try:
            product = Product.objects.get(sku=row['sku'])
            product.inventory_quantity = int(row['inventory_quantity'])
            product.save()
            updated.append(product.sku)
        except Product.DoesNotExist:
            continue
    return updated

@shared_task
def email_report(skus):
    send_mail(
        'Nightly Inventory Report',
        f'Updated products: {", ".join(skus)}',
        'from@example.com',
        ['admin@example.com']
    )
