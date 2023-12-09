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