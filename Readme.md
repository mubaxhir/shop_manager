# Shop Manager Backend

A simplified backend system built with **Python**, **Django**, and **Django REST Framework** for managing product data, integrating with Shopify webhooks, and performing nightly background tasks.

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

1. **Import:** Load mock product data from CSV
2. **Validate & Update:** Check data, update inventory
3. **Report:** Generate and email inventory update summary

## Setup Instructions

1. Clone repo & install Docker
2. Copy `.env.example` to `.env` and configure
3. Build and run:  
    ```sh
    docker-compose up --build
    ```
4. Access API at `http://localhost:8000/api/`

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

## Onboarding Plan (For Juniors)

1. **Project Overview:** Walkthrough of architecture and main components.
2. **Setup:** Guide through Docker setup and running tests.
3. **API Exploration:** Use tools like Postman to try endpoints.
4. **Codebase Tour:** Review models, views, serializers, and tasks.
5. **First Task:** Simple bug fix or test addition.

---

> **Note:** See individual files for detailed endpoint documentation.