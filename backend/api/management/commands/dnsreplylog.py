import re
from django.core.management.base import BaseCommand
from api.models import DNSLog
import time
from datetime import datetime



log_file_path = "/home/bewin/Projects/Backend-1/Sample/query.log"

class Command(BaseCommand):
    help = 'Check and add DNS log entries to the database'

    def handle(self, *args, **options):
        processed_entries = []

        def process_log_entry(entry):
            timestamp, action, details = entry
            a = details.split()
            date_string_with_year = f"2023 {timestamp}"
            datetime_object = datetime.strptime(date_string_with_year, "%Y %b %d %H:%M:%S")


            # Extracting values from log entry
            date_time = datetime_object
            # process_name = a[0]
            ip_address = a[0]
            domain_name = a[1]
            record_type = a[2]
            query_class = a[3]
            query_type = a[4]
            query_time = float(a[5])
            num_records = int(a[6])
            record_size = int(a[7])

            # Check if the entry already exists in the database
            if not DNSLog.objects.filter(date_time=date_time, ip_address=ip_address,
                                         domain_name=domain_name, record_type=record_type, query_class=query_class,
                                         query_type=query_type, query_time=query_time, num_records=num_records,
                                         record_size=record_size).exists():

                # Create and save a new DNSLog object
                dns_log_entry = DNSLog.objects.create(
                    date_time=date_time,
                    ip_address=ip_address,
                    domain_name=domain_name,
                    record_type=record_type,
                    query_class=query_class,
                    query_type=query_type,
                    query_time=query_time,
                    num_records=num_records,
                    record_size=record_size
                )
                dns_log_entry.save()

                print("New entry saved to the database")

            print("\n")

        def read_log_file(file_path):
            with open(file_path, 'r') as file:
                log_entries = file.read()
            matches = re.findall(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}) .* (reply): (.+)', log_entries)
            return matches

        while True:
            current_entries = read_log_file(log_file_path)

            new_entries = [entry for entry in current_entries if entry not in processed_entries]
            for entry in new_entries:
                process_log_entry(entry)
            processed_entries = current_entries
            time.sleep(1)
