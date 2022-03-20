from django.urls import path, include
from .views import (
    AddUserAPIViewset,
    AddClientAPIView,
    UpdateClientAPIView,
    DeleteClientAPIView,
    AddMailingAPIView,
    DeleteMailingAPIView,
    ListMailingGeneralAPIView,
    UpdateMailingAPIView,
    StartMailingAPIView
)

app_name = 'mailing'

urlpatterns = [
    # add urls
    path('add-client/', AddClientAPIView.as_view()),
    path('add-mailing/', AddMailingAPIView.as_view()),
    path('add-user/', AddUserAPIViewset.as_view()),

    # update urls
    path('update-client/<int:pk>', UpdateClientAPIView.as_view()),
    path('update-mailing/<int:pk>', UpdateMailingAPIView.as_view()),

    # delete urls
    path('delete-client/<int:pk>', DeleteClientAPIView.as_view()),
    path('delete-mailing/<int:pk>', DeleteMailingAPIView.as_view()),

    # list urls
    path('mailings/', ListMailingGeneralAPIView.as_view()),

    # send url
    path('send/<int:pk>', StartMailingAPIView.as_view())
]
