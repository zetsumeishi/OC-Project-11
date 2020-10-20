import csv
from unicodedata import normalize
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from product.constants import PRODUCT_FIELDS
from product.models import Product, Category


class Command(BaseCommand):
    help = "Imports CSV data into database."

    def handle(self, *args, **options):
        try:
            products = list()
            with open(settings.MODIFIED_CSV, newline="") as r:
                reader = csv.DictReader(r, delimiter=";")
                products_categories = list()

                for row in reader:
                    product_data = dict()
                    for field in PRODUCT_FIELDS:
                        if row[field].isdigit():
                            product_data[field] = Decimal(row[field])
                        elif field == "categories_tags":
                            categories = row[field].split(",")
                            category_obj_lst = list()
                            for category in categories:
                                category = (
                                    normalize("NFKD", category)
                                    .encode("ASCII", "ignore")
                                    .decode()
                                    .lower()[3:]
                                )
                                category_qs = Category.objects.filter(
                                    name=category
                                )
                                if category_qs:
                                    category_obj_lst.append(
                                        category_qs.first()
                                    )
                                else:
                                    category_obj = Category(name=category)
                                    category_obj.save()
                                    category_obj_lst.append(category_obj)
                        else:
                            product_data[field] = (
                                normalize("NFKD", row[field])
                                .encode("ASCII", "ignore")
                                .decode()
                                .lower()
                            )
                    already_added = [
                        product
                        for product in products
                        if product.product_name == product_data["product_name"]
                    ]
                    if not already_added:
                        products_categories.append(category_obj_lst)
                        products.append(Product(**product_data))
            Product.objects.bulk_create(products)
            products = Product.objects.all().order_by("id")
            for product, category_list in zip(products, products_categories):
                product.categories.set(category_list)
                product.save()
        except Exception as e:
            raise CommandError(f"Something went wrong.\n{e}")

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully imported data from CSV to database."
            )
        )
