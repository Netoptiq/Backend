from django.db import models
from django.utils import timezone
# Create your models here.
from django.db.models.signals import post_save
from django.dispatch import receiver
import fcntl
import os
 

class DNSLog(models.Model):
    date_time = models.DateTimeField()
    ip_address = models.GenericIPAddressField()
    domain_name = models.CharField(max_length=255)
    record_type = models.CharField(max_length=10)
    query_class = models.CharField(max_length=10)
    query_type = models.CharField(max_length=10)
    query_time = models.FloatField()
    num_records = models.IntegerField()
    record_size = models.IntegerField()
    latitude = models.CharField(max_length=200,blank="",default='')
    longitude = models.CharField(max_length=200,blank="",default='')

    def __str__(self):
        return f"{self.date_time} - {self.process_name} - {self.domain_name}"


# file_path = '/home/bewin/Projects/Backend-1/Sample/blacklist.conf'
file_path = '/etc/unbound/block.conf'

class Blacklist(models.Model):
    domain = models.CharField(max_length=200)

    def save(self, *args, **kwargs):
        with open(file_path, "a") as file:
            try:
                print(self.domain)
                fcntl.flock(file, fcntl.LOCK_EX)
                file.write(f'local-zone: "{self.domain}" refuse\n')
                # file.write(f'local-zone: "{self.domain}" redirect\n')
                # file.write(f'local-data: "{self.domain} A 0.0.0.0"\n')
            finally:
                fcntl.flock(file, fcntl.LOCK_UN)
        super().save(*args, **kwargs)




class DGADetechted(models.Model):
    domain = models.CharField(max_length=200)



class ThreatIntel(models.Model):
    indicator = models.CharField(max_length=255)
    threat_level = models.CharField(max_length=50)

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     name = models.CharField(max_length=255)
#     email = models.CharField(max_length=255, unique=True)
#     password = models.CharField(max_length=255)
#     permission = models.CharField(max_length=255, default="")
#     username = None

#     USERNAME_FIELD = 'email'
#     REQUIRED_FIELDS = []

# class Domaincount(models.Model):
#     domain = models.CharField(max_length=100)
#     count = models.IntegerField(default=0,blank=0)

# class Query(models.Model):
#     ip = models.CharField(max_length=100)
#     domain = models.CharField(max_length=100)  # Fix the typo here
#     record = models.CharField(max_length=10)
#     country = models.CharField(max_length=5)

# class Delay(models.Model):
#     delay = models.FloatField()
    
# class Reply(models.Model):
#     ip = models.CharField(max_length=100)
#     domain = models.CharField(max_length=100)  # Fix the typo here
#     record = models.CharField(max_length=10)
#     res_type = models.CharField(max_length=10)
#     delay = models.FloatField()
#     TSIG = models.FloatField()
#     size = models.IntegerField()
#     country = models.CharField(max_length=5)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.update_delay_table()
    
#     def update_delay_table(self):
#         delay = self.delay
#         Delay.objects.create(delay = delay)

# class Log(models.Model):
#     datetime = models.DateTimeField()
#     query = models.ForeignKey(Query, models.CASCADE)
#     reply = models.ForeignKey(Reply, models.CASCADE)

#     def save(self, *args, **kwargs):
#         super().save(*args, **kwargs)
#         self.update_domain_count()

#     def update_domain_count(self):
#         domain = self.query.domain

#         domain_count, created = Domaincount.objects.get_or_create(domain=domain)

#         if not created:
#             domain_count.count += 1
#             domain_count.save()

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     MALE = 'Male'
#     FEMALE = 'Female'
#     GENDER_IN_CHOICES = [
#         (MALE, 'Male'),
#         (FEMALE, 'Female'),
#     ]
#     phone_number = models.CharField(max_length=20, blank=True, null=True, unique=True)
#     gender = models.CharField(max_length=6, choices=GENDER_IN_CHOICES, null=True, blank=True)
#     country = models.CharField(max_length=120, null=True, blank=True)
#     city = models.CharField(max_length=120, null=True, blank=True)
#     state = models.CharField(max_length=120, null=True, blank=True)
#     is_approved_to_be_in_touch = models.BooleanField(default=False)
        
