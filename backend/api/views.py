from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
# Create your views here.
import os
log_file_path = "E:\\Netoptiq - backend\\Sample\\dns_log_file.log"

class basic_analysis(APIView):
    def post(self, request):
        with open(log_file_path, 'r') as file:
            lines = file.readlines()
        line_count = len(lines)

        response= {
            'total_query':line_count
        }
        return Response(response)