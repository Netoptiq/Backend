from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('basiclog/',BasicAnalysis.as_view()),
    path('te/',LiveQuery.as_view()),
    path('a/',Total_query.as_view()),
    path('tw/',Livegraph.as_view()),
    path('td/',Highlyusedusers.as_view()),
    path('logs/', LogListAPIView.as_view(), name='log-list'),
    path('query/', DNSLogQueryCountView.as_view(), name='query-count'),
]