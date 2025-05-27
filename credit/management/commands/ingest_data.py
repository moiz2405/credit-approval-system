# credit.management.commands.ingest_data.py
from django.core.management.base import BaseCommand
from credit.tasks import ingest_customer_data, ingest_loan_data

class Command(BaseCommand):
    help = 'Trigger ingestion of customer and loan data'

    def handle(self, *args, **kwargs):
        ingest_customer_data.delay()
        ingest_loan_data.delay()
        self.stdout.write(self.style.SUCCESS('Data ingestion tasks triggered'))
