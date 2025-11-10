from django.urls import path
from api.views import SendEmailRegistrationAPiVIew

urlpatterns = [
    path('sign-in/', SendEmailRegistrationAPiVIew.as_view())
]
