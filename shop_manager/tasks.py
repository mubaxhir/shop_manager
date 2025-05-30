from celery import chain, shared_task


@shared_task
def nightly_task_chain():
    from products.tasks import import_csv_data, validate_and_update_inventory, send_report_email
    file_path = 'test.csv'  # adjust path

    chain(
        import_csv_data.s(file_path) |
        validate_and_update_inventory.s() |
        send_report_email.s()
    ).apply_async()
