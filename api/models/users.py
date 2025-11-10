from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import FileExtensionValidator
from django.utils import timezone
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
    
class UserConfrimation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='confrimations')
    code = models.PositiveIntegerField()
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
    