### Old Script ###

# import re
# from datetime import datetime
# from django.utils import timezone
# from django.core.management.base import BaseCommand
# from api.models import Log, Query, Reply,Domaincount
# #
# class Command(BaseCommand):
#     help = 'Parse and save logs into Django models'

#     def handle(self, *args, **options):
#         log_file_path = "/home/bewin/Projects/Backend-1/Sample/query.log"

#         current_query = None  

#         try:
#             with open(log_file_path, 'r') as f:
#                 for entry in f.readlines():
#                     match = re.match(r'(\w{3} \d{2} \d{2}:\d{2}:\d{2}) .* (query|reply): (.+)', entry)
#                     if match:
#                         log_datetime_str, log_type, log_data = match.groups()

#                         # Parse the date and time and make it timezone-aware
#                         log_datetime = timezone.make_aware(datetime.strptime(log_datetime_str + ' 2023', '%b %d %H:%M:%S %Y'))

#                         if log_type == 'query':
#                             # Process the query
#                             query_data = log_data.split()
#                             current_query = {
#                                 'ip': query_data[0],
#                                 'domain': query_data[1],
#                                 'record': query_data[2],
#                                 'country': query_data[3],
#                             }

#                             # Create or retrieve Query instance
#                             query_instance, _ = Query.objects.get_or_create(**current_query)
#                         elif log_type == 'reply' and current_query:
#                             # Process the reply
#                             reply_data = log_data.split()

#                             # Create or retrieve Reply instance
#                             reply_instance, _ = Reply.objects.get_or_create(
#                                 ip=reply_data[0],
#                                 domain=reply_data[1],
#                                 record=reply_data[2],
#                                 country=reply_data[3],
#                                 res_type=reply_data[4],
#                                 delay=float(reply_data[5]),
#                                 TSIG=float(reply_data[6]),
#                                 size=int(reply_data[7]),
#                             )

#                             # Check if the Log entry already exists
#                             log_instance, created = Log.objects.get_or_create(
#                                 datetime=log_datetime,
#                                 reply=reply_instance,
#                                 query=query_instance,
#                             )
                            

#                             # Reset current_query after processing the reply
#                             current_query = None

#         except FileNotFoundError:
#             print(f"Error: File not found - {log_file_path}")
#         except Exception as e:
#             print(f"An error occurred: {e}")

#         print('Success: Log entries parsed and models created.')
