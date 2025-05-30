from celery import shared_task, chain
from django.db import transaction
from django.core.mail import send_mail
from .models import Product
import csv
import io

@shared_task
def import_csv_data(file_path):
    """
    Task 1: Reads mock product data from CSV.
    Expects a file with headers: sku,inventory_quantity
    Returns: list of dicts
    """
    with open(file_path, 'r') as f:
        decoded = f.read()
        reader = csv.DictReader(io.StringIO(decoded))
        data = [row for row in reader]
    return data


@shared_task
def validate_and_update_inventory(data):
    """
    Task 2: Validates & updates product inventory.
    Returns: summary dict with counts.
    """
    updated = []
    skipped = []

    with transaction.atomic():
        for row in data:
            try:
                sku = row['sku']
                qty = int(row['inventory_quantity'])
                product = Product.objects.get(sku=sku)
                product.inventory_quantity = qty
                product.save()
                updated.append({'sku': sku, 'qty': qty})
            except (Product.DoesNotExist, ValueError, KeyError):
                skipped.append(row)

    return {
        'updated': updated,
        'skipped': skipped,
    }


@shared_task
def send_report_email(summary):
    """
    Task 3: Sends email with summary of updates.
    """
    updated = summary['updated']
    skipped = summary['skipped']

    message = f"Inventory Update Summary:\n\nUpdated: {len(updated)} products\nSkipped: {len(skipped)} rows\n\n"

    if updated:
        message += "Updated SKUs:\n"
        for item in updated:
            message += f"  {item['sku']} -> {item['qty']}\n"

    if skipped:
        message += "\nSkipped rows:\n"
        for item in skipped:
            message += f"  {item}\n"
            
    print("Sending report email...")
    print(message)

    # Replace with your actual email settings
    send_mail(
        subject="Nightly Inventory Update Report",
        message=message,
        from_email="noreply@yourdomain.com",
        recipient_list=["admin@yourdomain.com"],
        fail_silently=False,
    )

    return "Report email sent."
