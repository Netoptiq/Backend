from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
import os
import re
from collections import deque
from rest_framework import status
from .models import *
from .Serializers import *
from datetime import datetime, timedelta
from collections import Counter
from django.db.models import Count


log_file_path = "E:\\Netoptiq - backend\\Sample\\dns_log_file.log"

class Test(APIView):
    def post(self, request):
        dns_record_pattern = re.compile(r'IN\s+([\w.-]+)\s+([+-])')
        dns_record_counts = {}
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
            for line in lines:
                match = dns_record_pattern.search(line)
                if match:
                    record_type = match.group(1)  # Extract the first group: record type
                    # sign = match.group(2)  # Extract the second group: '+' or '-'
                    
                    if 'IN' in line and '+' in line:
                        key = f"{record_type}"
                        dns_record_counts[key] = dns_record_counts.get(key, 0) + 1

        line_count = len(lines)
        response = {
            'total_query': line_count,
            'dns_record_counts': dns_record_counts,
        }
        return Response(response)

class BasicAnalysis(APIView):
    def get(self, request):
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
        line_count = len(lines) 
        
        response = {
            'query': line_count
        }
        return Response(response)



class LiveQuery(APIView):
    def post(self, request):
        log_file_path = "E:\\Netoptiq - backend\\Sample\\dns_log_file.log"
        num_last_lines = 10
        last_lines_buffer = deque(maxlen=num_last_lines)
        with open(log_file_path, 'r') as file:
            for line in file:
                last_lines_buffer.append(line)
        last_10_lines = list(last_lines_buffer)
        response = {
            'last_10_lines': last_10_lines,
        }
        return Response(response)
    
class DNSLogQueryCountView(APIView):
    def get(self, request, format=None):
        log_file_path = "E:\\Netoptiq - backend\\Sample\\unbound.log"

        f = open(log_file_path, 'r')
        a = f.readlines()
        # try:
        #     with open(log_file_path, 'r') as log_file:
        #         log_entries = log_file.readlines()
        # except FileNotFoundError:
        #     return Response({"error": "Log file not found"}, status=status.HTTP_404_NOT_FOUND)

        # Regular expression to match queries
        query = re.findall('query:',a)

        # Count the number of queries using regular expressions
        print(len(query))
        # return Response("dwadwa")
        # return Response({"total_queries": len(query)}, status=status.HTTP_200_OK)


###########################################################################################################################

#realtime log
class LogListAPIView(APIView):
    def get(self, request, format=None):
        logs = Log.objects.all()
        serializer = LogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class Livegraph(APIView):
    def get(self, request, *args, **kwargs):
        try:
            thirty_seconds_ago = timezone.now() - timezone.timedelta(seconds=30)
            count = Log.objects.filter(datetime__gt=thirty_seconds_ago ).count()
            return Response({'count': count}, status=status.HTTP_200_OK)
        
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

     
class Highlyusedusers(APIView):
    def get(self,request):
        ip_counter = Counter(Query.objects.values_list('ip', flat=True))
        # top_ips = ip_counter.most_common(6)
        return Response(ip_counter)

class Total_query(APIView):
    def get(self, request):
        total_count = Log.objects.count()
        return Response(total_count)
