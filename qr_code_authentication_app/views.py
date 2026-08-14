# qr_code_authentication_app/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile

import pyotp
import qrcode



# qr_code_authentication_app/views.py

from django.shortcuts import render
from authOP.globals import qr_auth
# def home(request):
#     return render(request, 'home.html')

from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .models import Profile
import pyotp
import qrcode
from io import BytesIO
import base64

from django.contrib.auth.decorators import login_required

# @login_required()
# def home(request):
#     if request.user.is_authenticated:
#         user = request.user
#         if user is not None:
#             if user.is_authenticated:
#                 user=request.user
#                 fname=user.first_name
#
#
#                 return render(request, "authentication/home.html", {'fname': fname,'ts_toggle':user.profile.qr_auth})
#             else:
#                 return render(request, "authentication/signin.html")
#         else:
#             return render(request, "authentication/signin.html")
#     else:
#         return render(request, "authentication/signin.html")
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def home(request):
    if request.user.is_authenticated:
        user = request.user

        if user is not None:
            if user.is_authenticated:
                user=request.user
                user_full_name=user.get_full_name()
                print("user name is ",user_full_name)
                fname=user.first_name
                print(user.profile.qr_auth)
                ts_toggle=user.profile.qr_auth
                return render(request, "authentication/home.html", {'user_full_name': user_full_name,'ts_toggle':ts_toggle})
            else:
                return render(request, "authentication/signin.html")
        else:
            return render(request, "authentication/signin.html")
    else:
        return redirect(reverse('signin'))
# views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

@login_required
def fetch_dashboard_data(request):
    user = request.user
    data = {
        'fname': user.first_name if user.first_name else '',
        'ts_toggle': user.profile.qr_auth if hasattr(user, 'profile') else False,
        # Add more data as needed
    }
    return JsonResponse(data)





# @login_required
# def register(request):
#     user = request.user
#
#     # qr code generation
#     username = user.username
#     email = user.email
#
#     # Check if the user already has a Profile object
#     profile, created = Profile.objects.get_or_create(user=user)
#
#     # If the profile was just created, generate OTP and update it
#     if created:
#         otp_secret = pyotp.random_base32()
#         profile.otp_secret = otp_secret
#         profile.save()
#     else:
#         otp_secret = profile.otp_secret
#
#     # Generate QR code
#     totp = pyotp.totp.TOTP(otp_secret)
#     provisioning_uri = totp.provisioning_uri(username, issuer_name='MyApp')
#     img = qrcode.make(provisioning_uri)
#
#     # Convert the image to a base64 string
#     img_buffer = BytesIO()
#     img.save(img_buffer)
#     img_buffer.seek(0)
#     img_str = base64.b64encode(img_buffer.getvalue()).decode()
#
#
#     return render(request, 'otp_verification.html', {'img_str': img_str})
#



from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from qr_code_authentication_app.models import Profile
import pyotp
import qrcode
import base64
from io import BytesIO

@login_required
def register(request):
    user = request.user

    # Check if the user already has a Profile object
    profile, created = Profile.objects.get_or_create(user=user)

    # If the profile was just created or if otp_secret is not set, generate OTP and update it
    if created or not profile.otp_secret:
        otp_secret = pyotp.random_base32()
        profile.otp_secret = otp_secret
        profile.save()
    else:
        otp_secret = profile.otp_secret

    # qr code generation
    username = user.username
    email = user.email

    # Generate QR code
    totp = pyotp.totp.TOTP(otp_secret)
    provisioning_uri = totp.provisioning_uri(username, issuer_name='MyApp')
    img = qrcode.make(provisioning_uri)

    # Convert the image to a base64 string
    img_buffer = BytesIO()
    img.save(img_buffer)
    img_buffer.seek(0)
    img_str = base64.b64encode(img_buffer.getvalue()).decode()

    return render(request, 'otp_verification.html', {'img_str': img_str})



from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
import pyotp
from django.contrib.auth import authenticate,login
from django.contrib import messages
# def qr_login(request):
#     username=request.GET.get('username')
#     user=request.user
#     print(user)
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         otp = request.POST.get('otp')
#
#         try:
#             user = User.objects.get(username=username)
#         except User.DoesNotExist:
#             messages.success(request, "User does not exist")
#             return render(request, 'login.html')
#
#         totp = pyotp.TOTP(user.profile.otp_secret)
#         if totp.verify(otp):
#             # OTP is valid, redirect to home page
#             login(request, user)
#             return redirect('home') # Use redirect() with the URL name 'home'
#         else:
#             messages.success(request, "Invalid OTP")
#             return render(request, 'login.html')
#
#     return render(request, 'login.html',{'username':username})


def qr_login(request):
    username = request.session.get('username')
    print(username)
    if not username:
        messages.error(request, "Session expired or invalid access.")
        return redirect('signin')
    if request.method == 'POST':
        # username = request.POST.get('username')
        request.session.get('username')
        otp = request.POST.get('otp')

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            messages.success(request, "User does not exist")
            return render(request, 'login.html')

        totp = pyotp.TOTP(user.profile.otp_secret)
        if totp.verify(otp):
            # OTP is valid, redirect to home page
            login(request, user)
            return redirect('home') # Use redirect() with the URL name 'home'
        else:
            messages.error(request, "Invalid OTP")
            return render(request, 'login.html')

    return render(request, 'login.html',{'username':username})

# from django.contrib import messages
#
# def qr_login(request, username):
#     print(username*50)
#
#     if request.method == 'POST':
#         otp = request.POST.get('otp')
#
#         try:
#             user = User.objects.get(username=username)
#
#         except User.DoesNotExist:
#             return render(request, 'login.html', {'error_message': 'User does not exist'},{'username': username})
#
#         totp = pyotp.TOTP(user.profile.otp_secret)
#         if totp.verify(otp):
#             # OTP is valid, log in the user
#             user = authenticate(username=username, password=user.password)  # Assuming user's password is stored properly
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')  # Redirect to the home page
#             else:
#                 print(username * 50)
#                 messages.error(request, "Invalid credentials")
#         else:
#             messages.error(request, "Invalid OTP")
#
#     return render(request, 'login.html', {'username': username})