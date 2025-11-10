from rest_framework.views import APIView
from rest_framework.response import Response
from api.utils import send_code_to_email
from api.serializers import EmailSerializer

class SendEmailRegistrationAPiVIew(APIView):
    serializer_class = EmailSerializer
    def post(self, request):
        email = request.data.get("email")
        send_code_to_email(email=email, code='0002')

        return Response({"message": "Habar yuborildi"})
    
