from django.urls import path
from api.views import SendEmailRegistrationAPiVIew, CodeVerifyAPiView,ResendCodeApiView,FullRegisterApiView

urlpatterns = [
    path('sign-up/', SendEmailRegistrationAPiVIew.as_view()),
    path('verify/', CodeVerifyAPiView.as_view()),
    path('resend-code/', ResendCodeApiView.as_view()),
    path('full-register/', FullRegisterApiView.as_view()),

]
