# qr_code_authentication_app/models.py

from django.db import models
from django.contrib.auth.models import User

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     otp_secret = models.CharField(max_length=16)  # Store OTP secret
#
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    otp_secret = models.CharField(max_length=16)  # Store OTP secret
    qr_auth = models.BooleanField(default=False)  # QR authentication flag
