# products/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('staff', 'Staff'),
    )
    user_type = models.CharField(
        max_length=20,
        choices=USER_TYPE_CHOICES,
        default='staff'
    )
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='products_user_set',
        blank=True,
        help_text='The groups this user belongs to.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='products_user_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"


class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, db_index=True)
    sku = models.CharField(max_length=100, unique=True, db_index=True)
    price = models.DecimalField(max_digits=10, decimal_places=2, db_index=True)
    inventory_quantity = models.IntegerField(db_index=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.sku})"


