from django.core.mail import send_mail
from config.settings import EMAIL_HOST_USER
def send_code_to_email(email, code):
    text = f"Assalamu alaykum, TwitterAPI uchun tasdiqlash kodingiz: {code}"
    send_mail(subject="Confirmaion code",
            message=text,
            from_email=EMAIL_HOST_USER,
            recipient_list=[email],
            fail_silently=False
            )
    
