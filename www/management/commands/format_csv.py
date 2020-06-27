import csv

from django.conf import settings
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = "Formats the CSV to be easier to import."

    def handle(self, *args, **options):
        try:
            with open(settings.RAW_CSV, newline="") as r, open(
                settings.MODIFIED_CSV, "w", newline=""
            ) as w:
                reader = csv.reader(r, delimiter="\t")
                writer = csv.writer(w, delimiter=";")

                # Reformat header
                for row in reader:
                    header = [
                        name.replace("-", "_").lstrip("_") for name in row
                    ]
                    break

                # Skip header before writing
                next(reader, None)

                writer.writerow(header)

                rows_count = 0
                for row in reader:
                    # Check if there's a nutriscore_grade and nova_group
                    if row[44] and row[45]:
                        rows_count += 1
                        writer.writerow(row)

        except Exception as e:
            raise CommandError(f"Something went wrong.\n{e}")

        self.stdout.write(
            self.style.SUCCESS(
                f"Successfully formatted CSV file. {rows_count} products kept."
            )
        )
