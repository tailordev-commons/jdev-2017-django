import csv
import os.path

from datetime import datetime
from decimal import Decimal as D
from django.core.management.base import BaseCommand, CommandError
from django.db.utils import IntegrityError

from temperature.models import Country, Record


def _import_record_from_csv_row(dt, temperature, uncertainty, country_name):
    """Import a record from a csv file row data"""

    country, _ = Country.objects.get_or_create(name=country_name)

    try:
        Record.objects.create(
            date=dt,
            temperature=temperature if len(temperature) else None,
            uncertainty=uncertainty if len(uncertainty) else None,
            country=country
        )
    except IntegrityError:
        # Unique constraint (date, country) raise an IntegrityError when trying
        # to save the same record twice. We ignore this error here as we want to
        # be able to run the load_records command more than once.
        pass


def load_data(csv_file_name):
    """Load data from input csv_file file"""

    # TODO
    # Optimize importation by using Record.objects.bulk_create on a country
    # basis
    with open(csv_file_name) as csv_file:
        dataset_reader = csv.DictReader(csv_file)
        for row in dataset_reader:
            _import_record_from_csv_row(*row.values())


class Command(BaseCommand):
    help = "Load temperature records from a csv file"

    def add_arguments(self, parser):
        parser.add_argument('CSV_FILE')

    def handle(self, *args, **options):
        csv_file_name = options['CSV_FILE']

        self.stdout.write(
            "Will import dataset from file: {}".format(csv_file_name)
        )

        # check that the file exists
        if not os.path.exists(csv_file_name):
            raise CommandError(
                "CSV file {} does not exists".format(csv_file_name)
            )

        load_data(csv_file_name)

        self.stdout.write(
            self.style.SUCCESS(
                "Temperature dataset has been successfully imported"
            )
        )
