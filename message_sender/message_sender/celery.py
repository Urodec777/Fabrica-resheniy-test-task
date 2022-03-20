import os
from celery import Celery

""" default celery settings """
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'message_sender.settings')
 
app = Celery('message_sender')
app.config_from_object('django.conf:settings', namespace='CELERY')
 
app.autodiscover_tasks()