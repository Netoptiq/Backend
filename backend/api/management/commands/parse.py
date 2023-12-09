import re
from django.core.management.base import BaseCommand
from api.models import Log, Query, Reply, Domaincount

class Command(BaseCommand):
    help = 'Parse and save logs into Django models'

    def handle(self, *args, **options):
        log_file_path = "E:\\Netoptiq - backend\\Sample\\query.log"

        current_query = None  # To store the current query while processing replies

        try:
            with open(log_file_path, 'r') as f:
                for entry in f.readlines():
                    match = re.match(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}) .* (query|reply): (.+)', entry)
                    if match:
                        log_datetime_str, log_type, log_data = match.groups()

                        if log_type == 'query':
                            # Process the query
                            query_data = log_data.split()
                            current_query = {
                                'ip': query_data[0],
                                'domain': query_data[1],
                                'record': query_data[2],
                                'country': query_data[3],
                            }
                        elif log_type == 'reply' and current_query:
                            # Process the reply
                            reply_data = log_data.split()
                            reply_instance = Reply.objects.create(
                                ip=reply_data[0],
                                domain=reply_data[1],
                                record=reply_data[2],
                                country=reply_data[3],
                                res_type=reply_data[4],
                                delay=float(reply_data[5]),
                                TSIG=float(reply_data[6]),
                                size=int(reply_data[7]),
                            )

                            # Create Log instance only if both Query and Reply instances are available
                            query_instance, created = Query.objects.get_or_create(**current_query)

                            if created:
                                Log.objects.create(query=query_instance, reply=reply_instance)

                            # Update or create Domaincount entry
                            domain_count, created = Domaincount.objects.get_or_create(
                                domains=current_query['domain'],
                                client=current_query['ip'],
                            )

                            if not created:
                                domain_count.count += 1
                                domain_count.save()

                            # Reset current_query after processing the reply
                            current_query = None

            print('Success: Log entries parsed and models created.')
        except FileNotFoundError:
            print(f"Error: File not found - {log_file_path}")
        except Exception as e:
            print(f"An error occurred: {e}")
