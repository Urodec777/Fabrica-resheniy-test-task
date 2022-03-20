from django.contrib.auth import get_user_model
from django.db import models
from django.utils import timezone
from django.core.mail import send_mail

def send_email(message, user):
    sender = 'youremail@gmail.com'
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

User = get_user_model() # get user model 


class Tag(models.Model):
    """ Tag model to filter mailing """
    name = models.CharField(max_length=256, verbose_name="Tag's name", unique=True)

    def __str__(self):
        return self.name


class Mailing(models.Model):
    """ Mailing model """
    tag = models.ForeignKey(Tag, on_delete=models.SET_NULL, null=True, related_name='tag', verbose_name="Tag's name")
    text = models.TextField(verbose_name="Mailing's text")
    start_mailing_date = models.DateTimeField(verbose_name='When start mailing')
    stop_mailing_date = models.DateTimeField(verbose_name='When stop mailing')
    count_of_sended_messages = models.IntegerField(verbose_name="Count of sended messages", null=True, default=0)

    def __str__(self):
        return self.text

    """ Method to start mailing with property decorator for easy of use """
    @property
    def start_mailing(self):
        users = self.tag.tags.all()
        for user in users:
            user_instance = User.objects.filter(username = user)
            client_qs = Client.objects.filter(username = user_instance.first())
            if client_qs.exists():
                client = client_qs.first()
            if not Message.objects.filter(mailing_id = self, clients_id = client).exists():
                email = send_email(self.text, user)
            if email == True:
                if not Message.objects.filter(mailing_id = self, clients_id = client).exists():
                    Message.objects.update_or_create(
                        sent_date = timezone.now(),
                        status = True,
                        clients_id = client,
                        mailing_id = self
                    )
            else:
                if not Message.objects.filter(mailing_id = self, clients_id = client).exists():
                    Message.objects.update_or_create(
                        sent_date = timezone.now(),
                        status = False,
                        clients_id = client,
                        mailing_id = self
                    )

            self.count_of_sended_messages += 1

    """ Method to check "start_mailing_date" field and as a result call "start_mailing" method. Method with property decorator for easy of use """
    @property
    def check_time(self):
        if timezone.now() >= self.start_mailing_date:
            self.start_mailing

class Client(models.Model):
    """ Client model """
    username = models.ForeignKey(User,on_delete=models.CASCADE, verbose_name="Client", related_name='client')
    phone_number = models.CharField(max_length=12, verbose_name="Client's phone number")
    provider_code = models.CharField(max_length=3, verbose_name="Clients's provider identificator")
    tags = models.ManyToManyField(Tag, verbose_name="Client's tags", related_name='tags')
    time_zone = models.CharField(max_length=30, verbose_name="Client's timezone")

    def __str__(self):
        return self.username.username


class Message(models.Model):
    """ Message model """
    sent_date = models.DateTimeField(verbose_name="The message was sent")
    status = models.BooleanField(verbose_name="Status of message")
    clients_id = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name="Client's id", related_name="user_tag")
    mailing_id = models.ForeignKey(Mailing, on_delete=models.CASCADE,  related_name="mailings", verbose_name="Mailing's id")

    def __str__(self):
        return str(self.status) # because it's easier to distinguish messages
        
        