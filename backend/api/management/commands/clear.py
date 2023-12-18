from django.core.management.base import BaseCommand
from api.models import Blacklist,DNSLog

class Command(BaseCommand):
    help = 'Clear all details in the database'

    def handle(self, *args, **options):
        self.stdout.write("Deleting all data from the database...")

        # Clear data from Query model
        Blacklist.objects.all().delete()

        DNSLog.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Successfully cleared all details in the database"))
