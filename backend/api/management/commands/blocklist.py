# import re
# from django.core.management.base import BaseCommand
# from api.models import Blacklist

# class Command(BaseCommand):
#     help = 'Parse logs and update Blacklist database'

#     def handle(self, *args, **options):
#         # Path to your log file
#         log_file_path = '/home/bewin/Desktop/Projects/Backend-1/block.conf'
#         lines_to_skip = 0
#         # Open the log file
#         with open(log_file_path, 'r') as log_file:
#             # Regular expression to extract local-zone and domain/IP
#             pattern = re.compile(r'local-zone: "(.*?)" redirect')

#             # Read and process each line
#             for line in log_file:
#                 # Skip lines until reaching the desired line
#                 if lines_to_skip > 0:
#                     lines_to_skip -= 1
#                     continue
#                 lines_to_skip+=1
#                 # Find matches in the current line
#                 matches = re.findall(pattern, line)
#                 for match in matches:
#                     domain_or_ip = match
#                     print('Test', domain_or_ip)
#                     if not Blacklist.objects.filter(domain=domain_or_ip).exists():
#                         Blacklist.objects.create(domain=domain_or_ip)
#                         print('Success', domain_or_ip)
            
#         self.stdout.write(self.style.SUCCESS('Blacklist updated successfully'))



import re
from django.core.management.base import BaseCommand
from api.models import Blacklist

class Command(BaseCommand):
    help = 'Parse logs and update Blacklist database'

    def handle(self, *args, **options):
        # Path to your log file
        log_file_path = '/home/bewin/Desktop/Projects/Backend-1/output.conf'
        lines_to_skip = 0
        line_number = 0  # Initialize line number

        # Open the log file
        with open(log_file_path, 'r') as log_file:
            # Regular expression to extract local-zone and domain/IP
            pattern = re.compile(r'local-zone: "(.*?)" redirect')

            # Read and process each line
            for line in log_file:
                line_number += 1  # Increment line number for each line

                # Skip lines until reaching the desired line
                if lines_to_skip > 0:
                    lines_to_skip -= 1
                    continue
                lines_to_skip += 1

                # Find matches in the current line
                matches = re.findall(pattern, line)
                for match in matches:
                    domain_or_ip = match
                    print(f'Line {line_number}: Test {domain_or_ip}')
                    if not Blacklist.objects.filter(domain=domain_or_ip).exists():
                        Blacklist.objects.create(domain=domain_or_ip)
                        print(f'Line {line_number}: Success {domain_or_ip}')

        self.stdout.write(self.style.SUCCESS('Blacklist updated successfully'))