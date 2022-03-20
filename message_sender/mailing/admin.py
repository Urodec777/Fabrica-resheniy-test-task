from django.contrib import admin
from .models import Tag, Client, Mailing, Message

admin.site.register(Tag)
admin.site.register(Mailing)
admin.site.register(Client)
admin.site.register(Message)