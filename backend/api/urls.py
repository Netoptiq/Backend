from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # path('log/',LogView.as_view()),
    # path('tquery/',Total_query.as_view()),
    # path('lquery/',Livegraph.as_view()),
    # path('highlyuseduser/',Highlyusedusers.as_view()),
    # path('logs/', LogListAPIView.as_view(), name='log-list'),

    path('blacklist/',BlacklistView.as_view(), name = 'GET or POST blocklist domains'),
    path('report/',DNSLogReport.as_view(), name = 'Give all details between paticular date and time'),
    path('tsv/',Tsv.as_view(), name = 'find a zeek tsv format file'),

    path('parse/', PcapFileParseView.as_view(), name='pcap_file_parse'),
    path('domain/',Domain_data.as_view(), name = 'Virus toal'),
    path('whois/',WhoisAPI.as_view(), name = 'who is'),#domain
    path('rdomain/',Domain_Reputation.as_view(), name = 'api void'),
    path('log1/',LogView.as_view(), name = 'see all domain view'),
    path('location/',LocationAPI.as_view(), name = 'see all domain view'),
    # path('register/', UserRegistrationView.as_view(), name='user-registration'),
    path('test/', Test.as_view(), name='user-registration'),

    path('log/', LogListPagenationAPIView.as_view(), name='see all domain view by 10'),#http://localhost:8000/api/log1/?page=1

    # path('register', RegisterView.as_view()),
    # path('login', LoginView.as_view()),
    # path('user', UserView.as_view()),
    # path('logout', LogoutView.as_view()),
]