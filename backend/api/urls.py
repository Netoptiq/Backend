from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    # path('basiclog/',BasicAnalysis.as_view()),
    # path('query/',LiveQuery.as_view()),
    path('tquery/',Total_query.as_view()),
    path('lquery/',Livegraph.as_view()),
    path('highlyuseduser/',Highlyusedusers.as_view()),
    path('logs/', LogListAPIView.as_view(), name='log-list'),
    # path('query/', DomainInfoAPIView.as_view(), name='query-count'),
]