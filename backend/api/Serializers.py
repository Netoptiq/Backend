from rest_framework import serializers
from .models import *






# serializers.py

class DNSLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSLog
        fields = '__all__'

class BlacklistSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blacklist
        fields = '__all__'

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = DNSLog
        fields = ('ip_address','domain_name')


# class QuerySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Query
#         fields = '__all__'

# class ReplySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Reply
#         fields = '__all__'


# class LogSerializer(serializers.ModelSerializer):
#     query = QuerySerializer()
#     reply = ReplySerializer()

#     class Meta:
#         model = Log
#         fields = '__all__'

# class DomaincountSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Domaincount
#         fields = '__all__'

# class DelaySerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Delay
#         fields = '__all__'

# class PcapFileSerializer(serializers.Serializer):
#     pcap_file = serializers.FileField()
    

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'name', 'email', 'password', 'permission']
#         extra_kwargs = {
#             'password': {'write_only': True}
#         }

#     def create(self, validated_data):
#         password = validated_data.pop('password', None)
#         instance = self.Meta.model(**validated_data)
#         if password is not None:
#             instance.set_password(password)
#         instance.save()
#         return instance
        

# from rest_framework import serializers

# class ObtainTokenSerializer(serializers.Serializer):
#     username = serializers.CharField()
#     password = serializers.CharField()