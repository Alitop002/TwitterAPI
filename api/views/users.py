from rest_framework.views import APIView
from django.contrib.auth import authenticate
from api.utils import send_code_to_email
from api.serializers import EmailSerializer, CodeSerializer, LoginSerializer, FullRegisterSerializer
from api.models import User, CODE_VERIFIED, DONE
from rest_framework.permissions import IsAuthenticated
from api.utils import CustomRespone

class SendEmailRegistrationAPiVIew(APIView):
    serializer_class = EmailSerializer
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data.get("email")
        user = User.objects.create(
            email=email
        )
        send_code_to_email(email, code=user.create_verify_code())


        return CustomRespone.success(
            status = True,
            message = "Confirmation code has sent to email.",
            data = user.token()
        )
    
class CodeVerifyAPiView(APIView):
    serializer_class = CodeSerializer
    permission_classes = [IsAuthenticated, ]
    def post(self, request):
        user = request.user
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        code = serializer.validated_data.get('code')

        if self.verify_code(user, code):
            return CustomRespone.success(
                status = True,
                message = "Code verifired succefully",
                data=user.token()
            )
        
        return CustomRespone.error(
            status = False,
            message = "Code don't match or code expired"
        )
        
    def verify_code(self, user: User, code:int):
        confrimations =user.confrimations.order_by("-created_at").first()
        if confrimations.code == code and not confrimations.is_expire():
            user.status = CODE_VERIFIED
            user.save()
            return True
        

class LoginAPiView(APIView):
    serializer_class = LoginSerializer
    
    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user = authenticate(request, username = username, password=password)
        if user is not None:
            return CustomRespone.success(
                status =True,
                message =  "You logged in succefully.",
                data= user.token()
            )

        return CustomRespone.success(status=True, message="Username or email or password indvalid")

class ResendCodeApiView(APIView):
    permission_classes = [IsAuthenticated, ]

    def get(self, request):
        user = request.user
        confrimations =user.confrimations.order_by("-created_at").first()
        if  confrimations.is_expire():
            return CustomRespone.error(
                status=False,
                message="Code has not been expired"
            )
        
        send_code_to_email(user.email, code=user.create_verify_code())


        return CustomRespone.success(
            status = True,
            message = "Confirmation code has sent to your email.",
            data = user.token()
        ) 
    
class FullRegisterApiView(APIView):
    serializer_Class = FullRegisterSerializer
    permission_classes = [IsAuthenticated, ]

    def put(self, request):
        user = request.user
        serializer = self.serializer_Class
        serializer.is_valid(raise_exception=True)

        first_name = serializer.validated_data.get('first_name')
        last_name = serializer.validated_data.get('last_name')
        username = serializer.validated_data.get('username')
        password = serializer.validated_data.get('password')

        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.set_password(password)
        user.status = DONE
        user.save()
        
        data = {
            "first_name": first_name,
            "last_name":last_name,
            "email": user.email,
            "username": username
        }

        return CustomRespone.success(
            status=True,
            message="User has been registered successfully",
            data=data
        )
