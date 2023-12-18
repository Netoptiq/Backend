from django.core.management.base import BaseCommand
from api.models import Blacklist
import re
class Command(BaseCommand):
    help = 'Block domains in the blacklist'

    def handle(self, *args, **options):
        file_path = '/home/bewin/Projects/Backend-1/Sample/blacklist.conf'
        blacklist_domains = set(Blacklist.objects.values_list('domain', flat=True))

        with open(file_path, 'r') as file:
            file_content = file.read()

        file_domains = set(re.findall(r'local-zone: "(.*?)" redirect', file_content))

        domains_to_add = blacklist_domains - file_domains

        with open(file_path, 'a') as file:
            for new_domain in domains_to_add:
                file.write(f'\nlocal-zone: "{new_domain}" redirect\n')
                file.write(f'local-data: "{new_domain} A 127.0.0.1"\n')

        if domains_to_add:
            self.stdout.write(self.style.SUCCESS("Domains have been added to the file."))
        else:
            self.stdout.write(self.style.SUCCESS("All domains in the Blacklist model are already in the file."))
