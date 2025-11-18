from django.core.mail import send_mail
from rest_framework.response import Response
from config.settings import EMAIL_HOST_USER
from rest_framework import status as st
import re
def send_code_to_email(email, code):
    text = f"Assalamu alaykum, TwitterAPI uchun tasdiqlash kodingiz: {code}"
    send_mail(subject="Confirmaion code",
            message=text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
            )
    
class CustomRespone:
    @staticmethod
    def success(status, message,data=None):
        data = {
            "status": status,
            "message": message,
            "data":data

        }
        return Response(
            data = data,
            status = st.HTTP_200_OK
        )
    @staticmethod
    def error(status, message,data=None
              ):
        data = {
            "status": status,
            "message": message,
            "data": data

        }
        return Response(
            data = data,
            status = st.HTTP_400_BAD_REQUEST
        )
    
def username_or_email(user_input: str):
    return re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', user_input)


