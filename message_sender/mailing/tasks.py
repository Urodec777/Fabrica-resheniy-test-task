from celery import shared_task
from .models import Mailing
from django.utils import timezone

""" Task for checking active mailings """
@shared_task
def check_status_of_mailings():
    mailings = Mailing.objects.filter(stop_mailing_date__gte = timezone.now())
    for mailing in mailings:
        mailing.check_time