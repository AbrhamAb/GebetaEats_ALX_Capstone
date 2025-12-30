from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    ROLE_CUSTOMER = 'customer'
    ROLE_RESTAURANT = 'restaurant'

    ROLE_CHOICES = [
        (ROLE_CUSTOMER, 'Customer'),
        (ROLE_RESTAURANT, 'Restaurant'),
    ]

    role = models.CharField(
        max_length=20, choices=ROLE_CHOICES, default=ROLE_CUSTOMER)

    def is_customer(self):
        return self.role == self.ROLE_CUSTOMER

    def is_restaurant(self):
        return self.role == self.ROLE_RESTAURANT

    def __str__(self):
        return self.username
