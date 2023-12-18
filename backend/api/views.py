from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# Create your views here.
from scapy.all import rdpcap, IP, TCP, UDP

from rest_framework import status
from .models import *
from .Serializers import *

import requests
import pandas as pd
import json


# from collections import deque
# from datetime import datetime, timedelta
# from collections import Counter
# from django.db.models import Count
# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from django.conf import settings
# from django.core.files.storage import default_storage
# import os
# import re

# class Test1(APIView):
#     def post(self, request):
#         dns_record_pattern = re.compile(r'IN\s+([\w.-]+)\s+([+-])')
#         dns_record_counts = {}
#         with open(log_file_path, 'r') as file:
#             lines = file.readlines()
#             for line in lines:
#                 match = dns_record_pattern.search(line)
#                 if match:
#                     record_type = match.group(1)  # Extract the first group: record type
#                     # sign = match.group(2)  # Extract the second group: '+' or '-'
                    
#                     if 'IN' in line and '+' in line:
#                         key = f"{record_type}"
#                         dns_record_counts[key] = dns_record_counts.get(key, 0) + 1

#         line_count = len(lines)
#         response = {
#             'total_query': line_count,
#             'dns_record_counts': dns_record_counts,
#         }
#         return Response(response)

# class BasicAnalysis(APIView):
#     def get(self, request):
#         with open(log_file_path, 'r') as file:
#             lines = file.readlines()
#         line_count = len(lines) 
        
#         response = {
#             'query': line_count
#         }   
#         return Response(response)



# class LiveQuery(APIView):
#     def post(self, request):
#         log_file_path = "E:\\Netoptiq - backend\\Sample\\dns_log_file.log"
#         num_last_lines = 10
#         last_lines_buffer = deque(maxlen=num_last_lines)
#         with open(log_file_path, 'r') as file:
#             for line in file:
#                 last_lines_buffer.append(line)
#         last_10_lines = list(last_lines_buffer)
#         response = {
#             'last_10_lines': last_10_lines,
#         }
#         return Response(response)
    

    
# class DNSLogQueryCountView(APIView):
#     def get(self, request, format=None):
#         log_file_path = "E:\\Netoptiq - backend\\Sample\\unbound.log"

#         f = open(log_file_path, 'r')
#         a = f.readlines()
#         # try:
#         #     with open(log_file_path, 'r') as log_file:
#         #         log_entries = log_file.readlines()
#         # except FileNotFoundError:
#         #     return Response({"error": "Log file not found"}, status=status.HTTP_404_NOT_FOUND)

#         # Regular expression to match queries
#         query = re.findall('query:',a)

#         # Count the number of queries using regular expressions
#         print(len(query))
#         # return Response("dwadwa")
#         # return Response({"total_queries": len(query)}, status=status.HTTP_200_OK)


###########################################################################################################################

#realtime log


class LogView(APIView): #domain visited
    def get(self, request, format=None):
        logs = DNSLog.objects.all()
        serializer = DNSLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# class LogListAPIView(APIView):#all log
#     def get(self, request, format=None):
#         logs = Log.objects.all()
#         serializer = LogSerializer(logs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)



# class Livegraph(APIView): #query came last 30 sec
#     def get(self, request, *args, **kwargs):
#         try:
#             thirty_seconds_ago = timezone.now() - timezone.timedelta(seconds=30)
#             count = Log.objects.filter(datetime__gt=thirty_seconds_ago ).count()
#             return Response({'count': count}, status=status.HTTP_200_OK)
        
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
     
# class Highlyusedusers(APIView): #top 5 ip
#     def get(self,request):
#         ip_counter = Counter(Query.objects.values_list('ip', flat=True))
#         top_ips = ip_counter.most_common(6)
#         return Response(top_ips)

# class Total_query(APIView):#!!!!
#     def get(self, request, format=None):
#         logs = Log.objects.count()
#         # serializer = DomaincountSerializer(logs, many=True)
#         return Response(logs, status=status.HTTP_200_OK)

# class Domain_Count(APIView): #domain visited
#     def get(self, request, format=None):
#         logs = Domaincount.objects.all()
#         serializer = DomaincountSerializer(logs, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class DNSLogListCreateView(APIView):
#     def get(self, request, format=None):
#         dns_logs = DNSLog.objects.all()
#         serializer = DNSLogSerializer(dns_logs, many=True)
#         return Response(serializer.data)

#     def post(self, request, format=None):
#         serializer = DNSLogSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


# from rest_framework.views import APIView
# from rest_framework.response import Response
# import csv

# class Tsv(APIView):
#     def post(self, request):
#         # Assuming the file input field is named 'log'
#         parser = request.FILES['log']

#         # Initialize an empty list to store the JSON data
#         json_data = []

#         # Read the TSV file using the csv module
#         reader = csv.reader(parser, delimiter='\t')

#         # Assuming the first row of the TSV file contains headers
#         headers = next(reader)

#         # Iterate through each row in the TSV file and convert it to a dictionary
#         for row in reader:
#             row_data = {}
#             for i in range(len(headers)):
#                 row_data[headers[i]] = row[i]
#             json_data.append(row_data)

#         # Return the JSON data as a response
#         return Response(json_data)

############################+++++++++++++++++++++++++++++++++++++



class ReverseOrderPageNumberPagination(PageNumberPagination):
    page_size = 10  # Set your desired page size
    page_size_query_param = 'page_size'
    max_page_size = 100


class LogListPagenationAPIView(APIView): #log with pagination
    def get(self, request, format=None):
        logs = DNSLog.objects.all().order_by('-date_time')  # Assuming there's a timestamp field for sorting
        paginator = ReverseOrderPageNumberPagination()
        result_page = paginator.paginate_queryset(logs, request)
        serializer = DNSLogSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)



class PcapFileParseView(APIView):#pcap analysis
    def post(self, request):
        pcap_file = request.FILES['pcap_file']
        packets = rdpcap(pcap_file)
        parsed_packets = []
        i = 0
        for packet in packets:
            print(packet)
            i+=1
            packet_len = packet.len if 'len' in packet else ''
            packet_info = {
                'id': i,
                'time': packet.time,
                'src': packet[IP].src if packet.haslayer(IP) else '',
                'dst': packet[IP].dst if packet.haslayer(IP) else '',
                'len': packet_len,
                'malware': False,
            }
            if packet_info['dst'] !='' and Blacklist.objects.filter(domain=packet_info['dst']).exists():
                packet_info['malware'] = True
            if packet.haslayer(TCP):
                packet_info['proto'] = 'TCP'
                packet_info['sport'] = packet[TCP].sport
                packet_info['dport'] = packet[TCP].dport
            elif packet.haslayer(UDP):
                packet_info['proto'] = 'UDP'
                packet_info['sport'] = packet[UDP].sport
                packet_info['dport'] = packet[UDP].dport
            else:
                packet_info['proto'] = ''
                packet_info['sport'] = ''
                packet_info['dport'] = ''
            parsed_packets.append(packet_info)
        return Response({'packets': parsed_packets})


class Domain_data(APIView):
    def post(self, request):
        domain = request.data.get('domain')
        url = "https://www.virustotal.com/api/v3/domains/"+domain
        print(url)
        headers = {
            "accept": "application/json",
            "x-apikey": "448a7aa846555d7e5feeb97fe7e608e14cf903572b5472301ba8af9d1497a61e"
        }
        response = requests.get(url, headers=headers)

        return Response(response.json())
    
class Domain_Reputation(APIView):
    def post(self,request):
        domain = request.data.get('domain')
        apivoid_key = "80a92298bdd58e4a6bf116d0eb49587c63b486fc"
        url = f"https://endpoint.apivoid.com/domainbl/v1/pay-as-you-go/?key={apivoid_key}&host={domain}"
        response = requests.get(url)
        response.raise_for_status()
        
        return Response(response.json())


class WhoisAPI(APIView):
    def post(self,request):
        domain = request.data.get('domain')
        url = 'https://whoisjsonapi.com/v1/'+domain
        headers = {
            'Authorization': 'Bearer TvL6oFeiLyV2cmRlvg8NTbAGUC2G0F34ns2NuGLHkmv8Li8vIs6yDz6dqxRHYxf'
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            
            return Response(data)
        except requests.exceptions.RequestException as e:
            return Response(e)


class BlacklistView(APIView):
    def get(self,request):
        data = Blacklist.objects.all()
        serializers = BlacklistSerializer(data, many = True)
        return Response(serializers.data)
    
    def post(self,request):
        domain = request.data.get('domain')
        if Blacklist.objects.filter(domain = domain):
            return Response("Already exist in db", status=status.HTTP_200_OK)
        else:
            serializer = BlacklistSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    



class DNSLogReport(APIView):
    def post(self, request, *args, **kwargs):
        start_date_time = request.data.get('start_date_time')
        end_date_time = request.data.get('end_date_time')

        if not start_date_time or not end_date_time:
            return Response(
                {"error": "Please provide both start_date_time and end_date_time in the request data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date_time = timezone.datetime.fromisoformat(start_date_time)
            end_date_time = timezone.datetime.fromisoformat(end_date_time)
        except ValueError:
            return Response(
                {"error": "Invalid date-time format. Please provide dates in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        logs = DNSLog.objects.filter(
            date_time__gte=start_date_time,
            date_time__lte=end_date_time
        )

        serializer = DNSLogSerializer(logs, many=True)  # Use your serializer here

        return Response(serializer.data, status=status.HTTP_200_OK)
    

class Tsv(APIView):
    def post(self, request):
        parser = request.FILES['log']
        df = pd.read_csv(parser, sep='\t')
        json_data_from_csv = df.to_json(orient='records')
        try:
            data_from_csv = json.loads(json_data_from_csv)
        except json.JSONDecodeError as e:
            return Response({"error": f"Failed to parse JSON from TSV file: {str(e)}"}, status=400)
        return Response(data_from_csv)

