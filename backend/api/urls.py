from django.contrib import admin
from django.urls import path
from .views import *

urlpatterns = [
    path('new/',BasicAnalysis.as_view()),
    path('te/',LiveQuery.as_view())
]