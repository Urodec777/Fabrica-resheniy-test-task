from rest_framework import serializers
from .models import Client, Mailing, User, Message


""" Client and User """
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password',)


class ClientSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = "__all__"


class ClientUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Client
        fields = ('phone_number', 'provider_code', 'tags', 'time_zone')

""" Mailing Serializer """

class MailingSerializer(serializers.ModelSerializer):

    class Meta:
        model = Mailing
        exclude = ('count_of_sended_messages',)

class MessageStatusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Message
        fields = ('status', )

class MailingDetailSerializer(serializers.ModelSerializer):
    mailings = MessageStatusSerializer(many = True, read_only = True)
    
    class Meta:
        model = Mailing
        fields = ('tag', 'count_of_sended_messages', 'mailings')

