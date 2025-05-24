FROM python:3.10-slim

WORKDIR /app
COPY . .
RUN pip install --upgrade pip && pip install -r requirements.txt

CMD ["gunicorn", "shop_manager.wsgi:application", "--bind", "0.0.0.0:8000"]
