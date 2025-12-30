from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from decimal import Decimal

from restaurants.models import Restaurant
from menu.models import Category, MenuItem


class Command(BaseCommand):
    help = "Seed demo data: demo users, restaurant, categories, and menu items."

    def handle(self, *args, **options):
        User = get_user_model()

        owner, created = User.objects.get_or_create(
            username="demo_owner",
            defaults={"email": "owner@example.com", "role": "restaurant"},
        )
        if created:
            owner.set_password("password")
            owner.save()
            self.stdout.write(self.style.SUCCESS(
                "Created demo owner: demo_owner / password"))
        else:
            self.stdout.write("Demo owner already exists")

        customer, created = User.objects.get_or_create(
            username="demo_customer",
            defaults={"email": "customer@example.com", "role": "customer"},
        )
        if created:
            customer.set_password("password")
            customer.save()
            self.stdout.write(self.style.SUCCESS(
                "Created demo customer: demo_customer / password"))
        else:
            self.stdout.write("Demo customer already exists")

        rest, created = Restaurant.objects.get_or_create(
            name="Demo Pizza",
            defaults={
                "owner": owner,
                "description": "Delicious demo pizza and sides",
                "location": "Demo City",
            },
        )
        if created:
            self.stdout.write(self.style.SUCCESS(
                f"Created restaurant: {rest.name}"))
        else:
            self.stdout.write(f"Restaurant '{rest.name}' already exists")

        cat_pizza, _ = Category.objects.get_or_create(name="Pizza")
        cat_sides, _ = Category.objects.get_or_create(name="Sides")

        items = [
            {"name": "Margherita", "price": Decimal(
                "8.50"), "category": cat_pizza, "description": "Classic margherita with fresh basil."},
            {"name": "Pepperoni", "price": Decimal(
                "9.50"), "category": cat_pizza, "description": "Spicy pepperoni with cheese."},
            {"name": "Garlic Bread", "price": Decimal(
                "3.00"), "category": cat_sides, "description": "Toasted garlic bread."},
        ]

        for it in items:
            mi, created = MenuItem.objects.get_or_create(
                restaurant=rest,
                name=it["name"],
                defaults={
                    "price": it["price"],
                    "category": it["category"],
                    "description": it.get("description", ""),
                },
            )
            if created:
                self.stdout.write(self.style.SUCCESS(
                    f"Created menu item: {mi.name}"))
            else:
                self.stdout.write(f"Menu item '{mi.name}' already exists")

        self.stdout.write(self.style.SUCCESS("Demo data seeding complete."))
