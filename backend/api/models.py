from django.db import models
from django.utils import timezone
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver


class Domaincount(models.Model):
    domain = models.CharField(max_length=100)
    count = models.IntegerField(default=0,blank=0)

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
    datetime = models.DateTimeField()
    query = models.ForeignKey(Query, models.CASCADE)
    reply = models.ForeignKey(Reply, models.CASCADE)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.update_domain_count()

    def update_domain_count(self):
        domain = self.query.domain

        domain_count, created = Domaincount.objects.get_or_create(domain=domain)

        if not created:
            domain_count.count += 1
            domain_count.save()









