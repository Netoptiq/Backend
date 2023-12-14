from rest_framework import serializers
from .models import *

class QuerySerializer(serializers.ModelSerializer):
    class Meta:
        model = Query
        fields = '__all__'

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = '__all__'


class LogSerializer(serializers.ModelSerializer):
    query = QuerySerializer()
    reply = ReplySerializer()

    class Meta:
        model = Log
        fields = '__all__'

class DomaincountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domaincount
        fields = '__all__'

class DelaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Delay
        fields = '__all__'

class PcapFileSerializer(serializers.Serializer):
    pcap_file = serializers.FileField()
    

# serializers.py
from rest_framework import serializers
from .models import DNSLog

class DNSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSLog
        fields = '__all__'
