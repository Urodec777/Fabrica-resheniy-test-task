from django.core.mail import send_mail
from rest_framework.response import Response
from rest_framework.generics import *
from .models import Client, Mailing, Message, Tag, User
from .serializers import (
    ClientSerializer, 
    UserSerializer, 
    ClientUpdateSerializer,
    MailingSerializer,
    MailingDetailSerializer,
)
from django.utils import timezone

""" send email function """
def send_email(message, user):
    sender = 'armwrestlingschool@gmail.com'
    try: 
        send_mail(
            message[:10],
            message,
            sender,
            [user.username.email],
            fail_silently=False
        )
        return True
    except Exception as ex:
        print(f'Exception {ex} was raising')
        return False

""" Add VIEWS """

class AddUserAPIViewset(CreateAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()

class AddClientAPIView(CreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

class AddMailingAPIView(CreateAPIView):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

class StartMailingAPIView(CreateAPIView):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    def get(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        serializer = MailingSerializer(mailing)
        return Response(serializer.data)

    def perform_create(self, serializer):
        # code for send messages
        data = serializer.validated_data
        message = data['text']
        start_date = data['start_mailing_date']
        end_date = data['stop_mailing_date']
        tag = data['tag']
        tag = Tag.objects.get(name = tag)
        # block to check if mailing object exists and update them, otherwise create 
        mailing_qs = Mailing.objects.filter(text = message)
        if mailing_qs.exists():
            mailing = mailing_qs.first()
            mailing.tag = tag
            mailing.text = message
            mailing.start_mailing_date = start_date
            mailing.stop_mailing_date = end_date
            mailing.save()
        else:
            super().perform_create(serializer)
        

        id = mailing_qs.first() # variable for mailing instance
        users = tag.tags.all() # variable for tag's users
        
        for user in users:
            user_instance = User.objects.filter(username = user)
            client_qs = Client.objects.filter(username = user_instance.first())
            if client_qs.exists():
                client = client_qs.first()
            
            # condition to avoid spam for users, which have got message.
            if not Message.objects.filter(mailing_id = id, clients_id = client).exists():
                email = send_email(message=message, user=user)

            if email:
                Message.objects.update_or_create(
                    sent_date = timezone.now(),
                    status = True,
                    clients_id = client,
                    mailing_id = id
                )
            else:
                Message.objects.update_or_create(
                    sent_date = timezone.now(),
                    status = False,
                    clients_id = client,
                    mailing_id = id
                )

""" Update VIEWS """

class UpdateClientAPIView(UpdateAPIView, ListAPIView):
    serializer_class = ClientUpdateSerializer
    queryset = Client.objects.all()

    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        serializer = ClientUpdateSerializer(client)
        return Response(serializer.data) 
    
    
class UpdateMailingAPIView(UpdateAPIView, ListAPIView):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    def get(self, request, pk):
        mailing = Mailing.objects.get(pk=pk)
        serializer = MailingSerializer(mailing)
        return Response(serializer.data)

""" Delete VIEWS """

class DeleteClientAPIView(DestroyAPIView, ListAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()

    def get(self, request, pk):
        client = Client.objects.get(pk=pk)
        serializer = ClientUpdateSerializer(client)
        return Response(serializer.data)

class DeleteMailingAPIView(DestroyAPIView, ListAPIView):
    serializer_class = MailingSerializer
    queryset = Mailing.objects.all()

    def get(self, request, pk):
        client = Mailing.objects.get(pk=pk)
        serializer = MailingSerializer(client)
        return Response(serializer.data)


""" ListViews """

class ListMailingGeneralAPIView(ListAPIView):
    serializer_class = MailingDetailSerializer
    queryset = Mailing.objects.all()




