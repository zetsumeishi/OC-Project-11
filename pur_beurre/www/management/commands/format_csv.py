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

                for row in reader:
                    writer.writerow(row)
        except Exception as e:
            raise CommandError(f"Something went wrong.\n{e}")

        self.stdout.write(
            self.style.SUCCESS("Successfully formatted CSV file.")
        )
