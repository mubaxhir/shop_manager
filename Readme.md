# Shop Manager Backend
A Django REST Framework application for managing products, integrating with Shopify, and handling inventory updates. This project is designed to be a comprehensive backend solution for a shop management system, featuring product management, authentication, and background tasks.

## Features

- **Product Management:** CRUD endpoints for products (name, SKU, price, inventory, last updated).
- **Filtering & Search:** Filter/search products by price, SKU, name, and quantity.
- **Authentication:** Basic authentication, restricted to a specific user group.
- **Shopify Webhook:** Single endpoint to update inventory from Shopify callbacks.
- **Admin Customization:** Advanced filtering, bulk price updates in Django admin.
- **Nightly Tasks:** Celery task chain for importing, validating, updating inventory, and emailing reports.
- **Database:** Normalized schema, transactional integrity, optimized queries.
- **Testing:** Unit tests for APIs, webhooks, and Celery tasks.
- **Deployment:** Dockerized for easy setup.

## API Endpoints

- **Products:**  
    - `GET /api/products/` — List products  
    - `POST /api/products/` — Create product  
    - `GET /api/products/{id}/` — Retrieve product  
    - `PUT/PATCH /api/products/{id}/` — Update product  
    - `DELETE /api/products/{id}/` — Delete product  
    - Filtering/search: `?price=`, `?sku=`, `?name=`, `?quantity=`
- **Shopify Webhook:**  
    - `POST /webhook/inventory-update/` — Update inventory from Shopify
- **Discount:**  
    - `POST /discount/{id}/` — Add or update product discount

## Admin Interface

- Filter by SKU, name, last updated
- Bulk price update actions

## Nightly Background Tasks
### 🕑 Nightly Inventory Update (via Celery Task Chain)

This project includes a nightly task chain that performs the following steps:

1. **Imports** product inventory data from a mock CSV file.
2. **Validates and updates** existing products' inventory in the database.
3. **Generates and sends** a summary email report of updated and skipped entries.

#### 🔁 Celery Task Chain

The task chain is defined in `products/tasks.py` and includes:

```python
import_csv_data.s('test.csv') |
validate_and_update_inventory.s() |
send_report_email.s()
```

---

### 🛠 Running Nightly Task Chain via Cron

To run this chain automatically at **2:00 AM every day**, add the following cron job to your host system:

```bash
0 2 * * * docker-compose exec web python manage.py shell -c "from products.tasks import import_csv_data, validate_and_update_inventory, send_report_email; from celery import chain; chain(import_csv_data.s('test.csv') | validate_and_update_inventory.s() | send_report_email.s()).apply_async()"
```

> 📝 Make sure the CSV file exists at `test.csv` inside the Docker container, and that the Celery worker is running.

---

### 📧 Email Configuration

Update your `settings.py` with SMTP credentials to enable email delivery:

```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@example.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
```

## Setup Instructions

1. Clone repo & install Docker
2. Build and run:  
    ```sh
    docker-compose up --build
    ```
3. Access API at `http://localhost:8000/api/`

## Testing

Run tests with:
```sh
docker-compose run web python manage.py test
```

## Code Review Checklist (For Juniors)

- Are endpoints RESTful and documented?
- Are queries optimized (e.g., using `select_related`, `prefetch_related`)?
- Are class-based views and serializers used appropriately?
- Is authentication enforced?
- Are third-party packages used correctly?
- Are Celery tasks, chain trigger tested?
- Are unit tests comprehensive and passing?
- Are migrations applied and database schema normalized?
- Is the code style consistent with PEP 8?
- Are error handling and logging implemented?
- redundant code removed?
- code reuseable and modular?


## Onboarding Plan (For Juniors)

1. **Project Overview:** Walkthrough of architecture and main components.
2. **Setup:** Guide through Docker setup and running tests.
3. **API Exploration:** Use tools like Postman to try endpoints.
4. **Codebase Tour:** Review models, views, serializers, and tasks.
5. **First Task:** Simple bug fix or test addition.

---

> **Note:** See individual files for detailed endpoint documentation.