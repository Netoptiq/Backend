import re
from django.core.management.base import BaseCommand
from api.models import Blacklist

class Command(BaseCommand):
    help = 'Export Blacklist from the database to a file'
    
    def handle(self, *args, **options):
        # Path to the output file
        print(111)
