import re
from django.core.management.base import BaseCommand
from api.models import Blacklist

class Command(BaseCommand):
    help = 'Export Blacklist from the database to a file'
    
    def handle(self, *args, **options):
        # Path to the output file
        blacklist_file_path = 'blacklist.conf'
        i=1
        # Open the output file for writing
        with open(blacklist_file_path, 'w') as blacklist_file:
            # Write entries from the Blacklist model to the file
            print('dwa')
            for entry in Blacklist.objects.all():
                print(i)
                blacklist_file.write(f'local-zone: "{entry.domain}" redirect\n')
                blacklist_file.write(f'local-data: "{entry.domain} A 0.0.0.0"\n')
                self.stdout.write(self.style.SUCCESS(f'Exported entry: {entry.domain}'))
                i+=1

        self.stdout.write(self.style.SUCCESS(f'Blacklist exported to {blacklist_file_path} successfully'))
