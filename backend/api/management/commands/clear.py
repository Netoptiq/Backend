# api/management/commands/clear_logs.py

from django.core.management.base import BaseCommand
from api.models import Log, Query, Reply

class Command(BaseCommand):
    help = 'Clear all items from Log, Query, and Reply tables'

    def handle(self, *args, **options):
        # Delete all items from the Log table
        Log.objects.all().delete()

        # Delete all items from the Reply table
        Reply.objects.all().delete()

        # Delete all items from the Query table
        Query.objects.all().delete()

        self.stdout.write(self.style.SUCCESS('Successfully cleared all items from Log, Query, and Reply tables'))
