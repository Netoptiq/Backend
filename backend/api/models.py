from django.db import models
from django.utils import timezone
# Create your models here.

class Query(models.Model):
    ip = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)  # Fix the typo here
    record = models.CharField(max_length=10)
    country = models.CharField(max_length=5)

class Reply(models.Model):
    ip = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)  # Fix the typo here
    record = models.CharField(max_length=10)
    res_type = models.CharField(max_length=10)
    delay = models.FloatField()
    TSIG = models.FloatField()
    size = models.IntegerField()
    country = models.CharField(max_length=5)

class Log(models.Model):
    datetime = models.DateTimeField(auto_now_add=True)
    query = models.ForeignKey(Query, models.CASCADE)
    reply = models.ForeignKey(Reply, models.CASCADE)