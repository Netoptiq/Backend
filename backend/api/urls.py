from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('log/',LogView.as_view()),
   
    path('tquery/',Total_query.as_view()),
    path('lquery/',Livegraph.as_view()),
    path('highlyuseduser/',Highlyusedusers.as_view()),
    path('logs/', LogListAPIView.as_view(), name='log-list'),
    path('parse/', PcapFileParseView.as_view(), name='pcap_file_parse'),
    path('domain/',Domain_data.as_view()),
    path('whois/',WhoisAPI.as_view()),#domain
    path('rdomain/',Domain_Reputation.as_view()),
    path('reply/',DNSLogListCreateView.as_view()),
    
    path('log1/', LogListPagenationAPIView.as_view(), name=''),#http://localhost:8000/api/log1/?page=1
]