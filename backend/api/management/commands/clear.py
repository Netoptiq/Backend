from django.core.management.base import BaseCommand
from api.models import Query, Reply, Log, Domaincount

class Command(BaseCommand):
    help = 'Clear all details in the database'

    def handle(self, *args, **options):
        self.stdout.write("Deleting all data from the database...")

        # Clear data from Query model
        Query.objects.all().delete()

        # Clear data from Reply model
        Reply.objects.all().delete()

        # Clear data from Log model
        Log.objects.all().delete()

        # Clear data from Domaincount model
        Domaincount.objects.all().delete()

        self.stdout.write(self.style.SUCCESS("Successfully cleared all details in the database"))
