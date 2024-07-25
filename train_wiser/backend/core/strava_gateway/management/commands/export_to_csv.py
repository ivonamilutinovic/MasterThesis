import csv
from django.core.management.base import BaseCommand

from strava_gateway.models import StravaActivity


class Command(BaseCommand):
    help = 'Exports data to CSV file'

    def handle(self, *args, **kwargs):
        with open('training_data.csv', 'w', newline='') as csvfile:
            fieldnames = [field.name for field in StravaActivity._meta.fields]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for obj in StravaActivity.objects.all():
                writer.writerow({field: getattr(obj, field) for field in fieldnames})

        self.stdout.write(self.style.SUCCESS('Data successfully exported to training_data.csv'))
