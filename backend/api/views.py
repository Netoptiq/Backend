from django.shortcuts import render
from django.db.models import Count, F, Sum
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.pagination import PageNumberPagination

# Create your views here.
from scapy.all import rdpcap, IP, TCP, UDP, DNS, DNSQR

from rest_framework import status

from .models import *
from .Serializers import *

import requests
import pandas as pd
import json
from scapy.all import *



# from collections import deque
# from collections import Counter
# from django.db.models import Count
# from djangochannelsrestframework.generics import GenericAsyncAPIConsumer
# from django.conf import settings
# from django.core.files.storage import default_storage
# import os
# import re


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

class BlockListPagenationAPIView(APIView): #log with pagination
    def get(self, request, format=None):
        logs = Blacklist.objects.all().order_by('-id')  # Assuming there's a timestamp field for sorting
        paginator = ReverseOrderPageNumberPagination()
        result_page = paginator.paginate_queryset(logs, request)
        serializer = BlacklistSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

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
    

    def delete(self, request, instance_id, format=None):
        try:
                entry = Blacklist.objects.get(pk=instance_id)
                domain_to_delete = entry.domain
                # conf_file_path = '/home/bewin/Desktop/Projects/Backend-1/Sample/output.conf'
                conf_file_path = '/etc/unbound/block.conf'
                try:
                    with open(conf_file_path, 'r') as file:
                        conf_content = file.readlines()
                    found = False
                    updated_conf_content = []
                    for line in conf_content:
                        if domain_to_delete in line:
                            found = True
                            continue
                        updated_conf_content.append(line)

                    if not found:
                        return Response({"detail": f"The domain '{domain_to_delete}' does not exist in the conf file."}, status=status.HTTP_404_NOT_FOUND)
                    with open(conf_file_path, 'w') as file:
                        file.writelines(updated_conf_content)

                    return Response({"detail": f"Successfully deleted the domain '{domain_to_delete}' from the conf file."}, status=status.HTTP_200_OK)
                except Exception as e:
                    return Response({"detail": f"An error occurred: {str(e)}"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        except Exception as e:
            return Response('Not found')


class BlacklistSearch(APIView):
    def post(self,request):
        domain = request.data.get('domain')
        data = Blacklist.objects.filter(domain=domain)
        if data.exists():

            serializer = BlacklistSerializer(data, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response('The domain name not in blacklist')


class LogView(APIView): #domain visited
    def get(self, request, format=None):
        logs = DNSLog.objects.all()
        serializer = DNSLogSerializer(logs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class LocationAPI(APIView): #domain visited
    def get(self, request, *args, **kwargs):
        queryset = DNSLog.objects.all()
        serializer = LocationSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class PcapAnalysis(APIView):
    def post(self, request):
        pcap_file = request.FILES['pcap_file']
        packets = rdpcap(pcap_file)
        parsed_packets = []
        i = 0

        for packet in packets:
            if packet.haslayer(DNS):
                i += 1
                packet_len = packet.len if 'len' in packet else ''
                packet_info = {
                    'id': i,
                    'time': packet.time,
                    'src': packet[IP].src if packet.haslayer(IP) else '',
                    'dst': packet[IP].dst if packet.haslayer(IP) else '',
                    'len': packet_len,
                    'malware': False,
                    'domain': '',
                    'takake_query': None,
                }
                # Check for takake domain or blacklist match


                if DNS in packet and packet.haslayer(DNSQR):
                    dns_name = packet[DNSQR].qname.decode('utf-8')
                    packet_info['domain'] = dns_name[:-1]

                if Blacklist.objects.filter(domain=packet_info['domain']).exists():
                    packet_info['malware'] = True

                # Protocol and port information
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
                print(i)
        return Response({'packets': parsed_packets}, status=status.HTTP_200_OK)






class PcapAnalysisold(APIView):#pcap analysis
    def post(self, request):
        pcap_file = request.FILES['pcap_file']
        packets = rdpcap(pcap_file)
        parsed_packets = []
        i = 0
        for packet in packets:
            print(packet)
            i+=1
            count=0
            packet_len = packet.len if 'len' in packet else ''
            
            packet_info = {
                'id': i,
                'time': packet.time,
                'src': packet[IP].src if packet.haslayer(IP) else '',
                'dst': packet[IP].dst if packet.haslayer(IP) else '',
                'len': packet_len,
                'malware': False,
            }
            if Blacklist.objects.filter(domain=packet_info['dst']).exists():
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
        # return Response({'packets': parsed_packets})
        return Response(count)



class Domain_data(APIView):
    def post(self, request):
        domain = request.data.get('domain')
        url = "https://www.virustotal.com/api/v3/domains/"+domain
        headers = {
            "accept": "application/json",
            "x-apikey": "f2916acd2d70218c6f98397606c58d7b8451f226f3b025e7756940c2f2324053"
        }
        #448a7aa846555d7e5feeb97fe7e608e14cf903572b5472301ba8af9d1497a61e
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
            'Authorization': 'Bearer 2b2befac267da8539950afc6837f8cba0c09d630c1329faf3c40fa4e8fea4d2e'
        }# TvL6oFeiLyV2cmRlvg8NTbAGUC2G0F34ns2NuGLHkmv8Li8vIs6yDz6dqxRHYxf
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Raises an HTTPError for bad responses
            data = response.json()
            
            return Response(data)
        except requests.exceptions.RequestException as e:
            return Response(e)
    
    # Return Error response (Just for checking)
    # def post(self, request):    
    #     domain = request.data.get('domain')
    #     url = 'https://whoisjsonapi.com/v1/' + domain
    #     headers = {
    #         'Authorization': 'Bearer SkuV8uHXRMxfA7vTYATGpwIE2zyDPDh8OBIZo5k-hSIxBYGNHxU6mx5y_9o7Ycm'

    #     }#TvL6oFeiLyV2cmRlvg8NTbAGUC2G0F34ns2NuGLHkmv8Li8vIs6yDz6dqxRHYxf

    #     try:
    #         response = requests.get(url, headers=headers)
    #         response.raise_for_status()  # Raises an HTTPError for bad responses
    #         data = response.json()
    #         return Response(data)
    #     except requests.exceptions.RequestException as e:
    #         # Extract information from the exception
    #         error_message = str(e)
    #         status_code = getattr(e.response, 'status_code', None)
    #         response_content = getattr(e.response, 'text', None)

    #         # Print or log the error details
    #         print(f'HTTP error occurred: {status_code} - {error_message}')
    #         print(f'Response content: {response_content}')

    #         # Return an appropriate response to the client
    #         return Response({'error': 'An error occurred'}, status=status_code or 500)


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
    




class DNSReport(APIView):
    def post(self, request, *args, **kwargs):
        start_date_time = request.data.get('start_date_time')
        end_date_time = request.data.get('end_date_time')

        if not start_date_time or not end_date_time:
            return Response(
                {"error": "Please provide both start_date_time and end_date_time in the request data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            start_date_time = datetime.fromisoformat(start_date_time)
            end_date_time = datetime.fromisoformat(end_date_time)
        except ValueError:
            return Response(
                {"error": "Invalid date-time format. Please provide dates in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        logs = DNSLog.objects.filter(
            date_time__gte=start_date_time,
            date_time__lte=end_date_time
        )

        # Query for additional DNS server report details
        query_details = logs.values('query_type').annotate(
            total_queries=Count('query_type'),
            average_query_time=Sum('query_time') / Count('query_time'),
        )

        # Your existing serializer
        serializer = DNSLogSerializer(logs, many=True)

        # Combine the results into the final JSON response
        result = {
            'total_queries': logs.count(),
            'query_details': query_details,
            'query_logs': serializer.data,
            'dns_server_report': {
                'query_statistics': {
                    'total_queries': logs.count(),
                    'query_types': logs.values('query_type').annotate(count=Count('query_type')).order_by('-count')
                },
                'latency_and_response_time': {
                    'average_response_time': logs.aggregate(avg_response_time=Sum('query_time') / Count('query_time'))['avg_response_time'],
                    # Add more latency metrics as needed
                },
                # Add more sections for traffic sources, security metrics, cache utilization, etc.
            }
        }

        return Response(result, status=status.HTTP_200_OK)



class ZeekLogAnalysis(APIView):
    def post(self, request):
        try:
            uploaded_file = request.FILES['file']
            data = uploaded_file.read().decode('utf-8')
            lines = data.strip().split('\n')
            parsed_data = []
            for line in lines:
                json_data = json.loads(line)
                domain = json_data.get('query', '') 
                is_blocked = Blacklist.objects.filter(domain=domain).exists()
                json_data['is_available'] = not is_blocked
                parsed_data.append(json_data)

            return Response(parsed_data, status=status.HTTP_200_OK)

        except KeyError:
            return Response({'error': 'File not provided'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
class StixTaxi(APIView):
    def post(self, request):
        domain = request.data.get('domain')
        

        return Response(domain, status=status.HTTP_200_OK)



class DGADetechtedApi(APIView):

    def get(self, request):
        count = DGADetechted.objects.all().count()
        return Response({'count': count})

    

    def post(self, request):
        domain = request.data.get('domain')
        data = DGADetechted.objects.filter(domain=domain)
        serializer = DGADetechtedSerializer(data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('Invalid Input', status=status.HTTP_200_OK)


class Test(APIView):
    def post(self, request):
        domain = request.data.get('domain')
        data = Test.objects.filter(domain=domain)
        serializer = TestSerializer(data, many=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response('Invalid Input', status=status.HTTP_200_OK)




# class DNSLogReport(APIView):
#     # def post(self, request, *args, **kwargs):
#     #     start_date_time = request.data.get('start_date_time')
#     #     end_date_time = request.data.get('end_date_time')

#     #     if not start_date_time or not end_date_time:
#     #         return Response(
#     #             {"error": "Please provide both start_date_time and end_date_time in the request data."},
#     #             status=status.HTTP_400_BAD_REQUEST
#     #         )
        
#     #     try:
#     #         start_date_time = timezone.datetime.fromisoformat(start_date_time)
#     #         end_date_time = timezone.datetime.fromisoformat(end_date_time)
#     #     except ValueError:
#     #         return Response(
#     #             {"error": "Invalid date-time format. Please provide dates in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."},
#     #             status=status.HTTP_400_BAD_REQUEST
#     #         )

#     #     logs = DNSLog.objects.filter(
#     #         date_time__gte=start_date_time,
#     #         date_time__lte=end_date_time
#     #     )

#     #     serializer = DNSLogSerializer(logs, many=True)  # Use your serializer here
#     #     result= {
#     #         'total_query': logs.count(),
#     #         'query': serializer.data
            
#     #     }
#     #     return Response(result, status=status.HTTP_200_OK)

#     def post(self, request, *args, **kwargs):
#         start_date_time = request.data.get('start_date_time')
#         end_date_time = request.data.get('end_date_time')

#         if not start_date_time or not end_date_time:
#             return Response(
#                 {"error": "Please provide both start_date_time and end_date_time in the request data."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
        
#         try:
#             start_date_time = datetime.fromisoformat(start_date_time)
#             end_date_time = datetime.fromisoformat(end_date_time)
#         except ValueError:
#             return Response(
#                 {"error": "Invalid date-time format. Please provide dates in ISO 8601 format (YYYY-MM-DDTHH:MM:SS)."},
#                 status=status.HTTP_400_BAD_REQUEST
#             )

#         logs = DNSLog.objects.filter(
#             date_time__gte=start_date_time,
#             date_time__lte=end_date_time
#         )

#         serializer = DNSLogSerializer(logs, many=True)  # Use your serializer here
#         result = {
#             'total_query': logs.count(),
#             'query': serializer.data
#         }
#         return Response(result, status=status.HTTP_200_OK)
    

# class PcapAnalysis(APIView):#withoud domain
#     def post(self, request):
#         pcap_file = request.FILES['pcap_file']
#         packets = rdpcap(pcap_file)
#         parsed_packets = []
#         i = 0
#         for packet in packets:
#             if packet.haslayer(DNS):
#                 i +=1
#                 packet_len = packet.len if 'len' in packet else ''
#                 packet_info = {
#                     'id': i,
#                     'time': packet.time,
#                     'src': packet[IP].src if packet.haslayer(IP) else '',
#                     'dst': packet[IP].dst if packet.haslayer(IP) else '',
#                     'len': packet_len,
#                     'malware': False,
#                     'domain': 
#                 }
#                 if packet_info['dst'] !='' and Blacklist.objects.filter(domain=packet_info['dst']).exists():
#                     packet_info['malware'] = True
#                 if packet.haslayer(TCP):
#                     packet_info['proto'] = 'TCP'
#                     packet_info['sport'] = packet[TCP].sport
#                     packet_info['dport'] = packet[TCP].dport
#                 elif packet.haslayer(UDP):
#                     packet_info['proto'] = 'UDP'
#                     packet_info['sport'] = packet[UDP].sport
#                     packet_info['dport'] = packet[UDP].dport
#                 else:
#                     packet_info['proto'] = ''
#                     packet_info['sport'] = ''
#                     packet_info['dport'] = ''
#                 parsed_packets.append(packet_info)
#         return Response({'packets': parsed_packets})
    



# class Test(APIView):#all log
#     def get(self, request, format=None):
#         logs = Blacklist.objects.count()
#         serializer = BlacklistSerializer(logs, many=True)
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




# class Tsv(APIView):
#     def post(self, request):
#         parser = request.FILES['log']
#         df = pd.read_csv(parser, sep='\t')
#         json_data_from_csv = df.to_json(orient='records')
#         try:
#             data_from_csv = json.loads(json_data_from_csv)
#         except json.JSONDecodeError as e:
#             return Response({"error": f"Failed to parse JSON from TSV file: {str(e)}"}, status=400)
#         return Response(data_from_csv)



# import jwt, datetime
# from rest_framework.exceptions import AuthenticationFailed

# SECRET = '2egfi2h9urawdjfn'


# class RegisterView(APIView):

#     def post(self, request):
#         serializer = UserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         serializer.save()
#         return Response(serializer.data)


# class LoginView(APIView):
#     def post(self, request):
#         email = request.data['email']
#         password = request.data['password']

#         user = User.objects.filter(email=email).first()

#         if user is None:
#             raise AuthenticationFailed('User not found!')

#         if not user.check_password(password):
#             raise AuthenticationFailed('Incorrect password!')

#         payload = {
#             'id': user.id,
#             'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=240),
#             'iat': datetime.datetime.utcnow()
#         }

#         token = jwt.encode(payload, SECRET, algorithm='HS256')

#         response = Response()

#         response.set_cookie(key='jwt', value=token, httponly=True)
#         response.data = {
#             'jwt': token
#         }
#         return response


# class UserView(APIView):

#     def get(self, request):
#         token = request.COOKIES.get('jwt')

#         if not token:
#             raise AuthenticationFailed('Unauthenticated!')

#         try:
#             payload = jwt.decode(token, SECRET, algorithms=['HS256'])
#         except jwt.ExpiredSignatureError:
#             raise AuthenticationFailed('Unauthenticated!')

#         user = User.objects.filter(id=payload['id']).first()
#         serializer = UserSerializer(user)
#         return Response(serializer.data)


# class LogoutView(APIView):
#     def post(self, request):
#         print("***")
#         response = Response()
#         response.delete_cookie('jwt')
#         response.data = {
#             'message': 'success'
#         }
#         return response
        
# from django.contrib.auth import get_user_model
# from rest_framework import views, permissions, status
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response

# from .Serializers import ObtainTokenSerializer
# from .Serializers import UserSerializer
# from .authentication import JWTAuthentication

# User = get_user_model()

# class ObtainTokenView(views.APIView):
#     permission_classes = [permissions.AllowAny]
#     serializer_class = ObtainTokenSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         username_or_phone_number = serializer.validated_data.get('username')
#         password = serializer.validated_data.get('password')

#         user = User.objects.filter(username=username_or_phone_number).first()
#         if user is None:
#             user = User.objects.filter(phone_number=username_or_phone_number).first()

#         if user is None or not user.check_password(password):
#             return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

#         # Generate the JWT token
#         jwt_token = JWTAuthentication.create_jwt(user)

#         return Response({'token': jwt_token})
        

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

