from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
import os
import re

log_file_path = "E:\\Netoptiq - backend\\Sample\\dns_log_file.log"

class BasicAnalysis(APIView):
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

from collections import deque

class LiveQuery(APIView):
    def post(self, request):
        log_file_path = "E:\\Netoptiq - backend\\Sample\\dns_log_file.log"

        # Set the desired number of last lines to retrieve
        num_last_lines = 10

        # Use deque to maintain a rolling buffer of the last 10 lines
        last_lines_buffer = deque(maxlen=num_last_lines)

        with open(log_file_path, 'r') as file:
            for line in file:
                last_lines_buffer.append(line)

        # Retrieve the last 10 lines from the buffer
        last_10_lines = list(last_lines_buffer)

        response = {
            'last_10_lines': last_10_lines,
        }
        return Response(response)
    