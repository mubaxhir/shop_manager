from products.tasks import import_csv_data, validate_and_update_inventory, send_report_email
from celery import chain

file_path = 'test.csv'

chain(
    import_csv_data.s(file_path) |
    validate_and_update_inventory.s() |
    send_report_email.s()
).apply_async()
