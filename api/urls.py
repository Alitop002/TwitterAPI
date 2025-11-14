from django.urls import path
from api.views import SendEmailRegistrationAPiVIew

urlpatterns = [
    path('sign-up/', SendEmailRegistrationAPiVIew.as_view())
]
