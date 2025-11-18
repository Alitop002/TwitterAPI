from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken

import random
import uuid
NEW, CODE_VERIFIED, DONE = ('new', 'code_veridied', 'done')

class User(AbstractUser):
    status_choices = (
        (NEW, NEW),
        (CODE_VERIFIED, CODE_VERIFIED),
        (DONE, DONE)
    )
    phone_number = models.CharField(max_length=13, blank=True, null=True)
    status = models.CharField(max_length=20, default=NEW, choices=status_choices)
    image = models.ImageField(upload_to='user_images/', validators=[FileExtensionValidator(allowed_extensions=['png', 'jpg', 'jpeg'])], blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    address = models.CharField(max_length=603, blank=True, null=True)

    def __str__(self):
        return self.username
    
    def create_verify_code(self):
        code = "".join([str(random.randint(0, 10000) % 10) for _ in range(4)])
        UserConfrimation.objects.create(
            user_id=self.id,
            code=code
        )
        return code

    def save(self, *args, **kwargs):
        if not self.username:
            username = f"username-{uuid.uuid4()}"
            self.username = username

        if not self.password:
            password = f"password-{uuid.uuid4()}"
            self.password = password
            self.set_password(self.password)

        super(User, self).save(*args, **kwargs)

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            "access":str(refresh.access_token),
            "refresh":str(refresh)
        }
    


    # def check_pass(self):
    #     if not self.password:
    #         temp_password = f'password-{uuid.uuid4().__str__().split("-"[-1])}'
    #         self.password = temp_password
        
    
class UserConfrimation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confrimations')
    code = models.CharField(max_length=4)
    expire_time = models.DateTimeField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        self.expire_time = timezone.now()+timezone.timedelta(minutes=2)
        return super().save(*args, **kwargs)
    
    def is_expire(self):
        if self.expire_time > timezone.now():             
            return False
        return True
    
    def __str__(self):
        return f"{self.user.username} | {self.code}"
    