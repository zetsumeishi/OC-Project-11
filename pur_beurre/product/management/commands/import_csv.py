import csv
from decimal import Decimal

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from product.constants import PRODUCT_FIELDS
from product.models import Product


class Command(BaseCommand):
    help = "Imports CSV data into database."

    def handle(self, *args, **options):
        try:
            products = []
            with open(settings.MODIFIED_CSV, newline="") as r:
                reader = csv.DictReader(r, delimiter=";")
                for row in reader:
                    product_data = {}
                    for field in PRODUCT_FIELDS:
                        if row[field].isdigit():
                            product_data[field] = Decimal(row[field])
                        else:
                            product_data[field] = row[field]
                    products.append(Product(**product_data))
            Product.objects.bulk_create(products)
        except Exception as e:
            raise CommandError(f"Something went wrong.\n{e}")

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully imported data from CSV to database."
            )
        )
