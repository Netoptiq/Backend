from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [

    path('blacklist/search/',BlacklistSearch.as_view(), name = 'dns exist or not'),
    path('blacklist/',BlockListPagenationAPIView.as_view(), name = 'GET or POST blocklist domains'),
    path('blacklist/<int:instance_id>/',BlockListPagenationAPIView.as_view(), name = 'GET or POST blocklist domains'),
    path('report/',DNSLogReport.as_view(), name = 'Give all details between paticular date and time'),

    path('parse/', PcapAnalysisold.as_view(), name='pcap analysis for all dest ip '),

    path('domain/',Domain_data.as_view(), name = 'Virus toal'),
    path('whois/',WhoisAPI.as_view(), name = 'who is'),
    path('rdomain/',Domain_Reputation.as_view(), name = 'api void'),

    path('location/',LocationAPI.as_view(), name = 'see all domain view'),

    path('pcap/', PcapAnalysis.as_view(), name='pcap analysis for dns dest ip'),
    path('tsv/', ZeekLogAnalysis.as_view(), name='parse and send zeek dns.log'),

    path('log/', LogListPagenationAPIView.as_view(), name='see all domain view by 10'),
    path('dga/', DGADetechtedApi.as_view(), name='see all domain view by 10'),

    path('blocklist1/',BlacklistView.as_view(), name = 'see all domain view+ add value in db'),
    path('log1/',LogView.as_view(), name = 'see all domain view'),


    # path('test/',Test.as_view()),
    # path('tquery/',Total_query.as_view()),
    # path('lquery/',Livegraph.as_view()),
    # path('highlyuseduser/',Highlyusedusers.as_view()),
    # path('logs/', LogListAPIView.as_view(), name='log-list'),
    # path('tsv/',Tsv.as_view(), name = 'find a zeek tsv format file'),
    # path('register/', UserRegistrationView.as_view(), name='user-registration'),
    # path('test/', Test.as_view(), name='user-registration'),
    # path('register', RegisterView.as_view()),
    # path('login', LoginView.as_view()),
    # path('user', UserView.as_view()),
    # path('logout', LogoutView.as_view())
]