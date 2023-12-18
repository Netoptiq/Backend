# yourapp/management/commands/parse_logs.py
import re
from django.core.management.base import BaseCommand
from api.models import Blacklist

class Command(BaseCommand):
    help = 'Parse logs and update Blacklist database'

    def handle(self, *args, **options):
        # Path to your log file
        log_file_path = '/home/bewin/Projects/Backend-1/Sample/blacklist.conf'
        with open(log_file_path, 'r') as log_file:
            log_content = log_file.read()

        # Regular expression to extract local-zone and domain/IP
        pattern = re.compile(r'local-zone: "(.*?)" redirect')

        # Find all matches in the log content
        matches = re.findall(pattern, log_content)

        # Iterate through matches and update Blacklist database
        for match in matches:
            domain_or_ip = match
            Blacklist.objects.create(domain=domain_or_ip)

        self.stdout.write(self.style.SUCCESS('Blacklist updated successfully'))


