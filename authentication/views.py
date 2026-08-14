from django.contrib import messages
from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from authOP import settings

from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from qr_code_authentication_app.views import register
from .tokens import generate_token
from django.core.mail import EmailMessage,send_mail
from qr_code_authentication_app.models import Profile
from django.contrib.auth.decorators import login_required


from django.contrib.auth.decorators import login_required

# @login_required()
def home(request):
    if request.user.is_authenticated:
        user = request.user
        if user is not None:
            if user.is_authenticated:
                user=request.user
                user_full_name=user.get_full_name()
                users = User.objects.filter(username=user)
                print("user name is ",user_full_name)
                print(user.profile.qr_auth)
                ts_toggle=user.profile.qr_auth
                return render(request, "authentication/home.html", {'user_full_name': user_full_name,'ts_toggle':ts_toggle,'users':users})
            else:
                return render(request, "authentication/signin.html")
        else:
            return render(request, "authentication/signin.html")
    else:
        return redirect(reverse('signin'))






# def signup_view(request):
#     if request.method == "POST":
#         username=request.POST.get('username')
#         fname=request.POST['fname']
#         lname=request.POST['lname']
#         email=request.POST['email']
#         pass1=request.POST['pass1']
#         pass2=request.POST['pass2']
#         digit=len(pass1)
#
#
#
#         if digit<=8:
#             if digit<=8:
#                 messages.error(request, "Password shoulde be greater then 8")
#                 context={'username': username, 'fname': fname, 'lname': lname, 'email': email}
#                 return render(request, 'authentication/signup.html',context)
#
#         elif pass1 != pass2:
#
#              messages.error(request,"Passwords do not match")
#              context={'username': username, 'fname': fname, 'lname': lname, 'email': email}
#              return render(request, 'authentication/signup.html',context)
#
#         if User.objects.filter(username=username):
#             messages.error(request,"username already exist")
#             return redirect("home")
#
#         if User.objects.filter(email=email):
#             messages.error(request,"email already exist")
#             return redirect("home")
#
#         # if username.isalnum():
#         #     messages.error(request,"username should be alphanumeric")
#
#         myuser=User.objects.create_user(username,email,pass1)
#         myuser.first_name=fname
#         myuser.last_name=lname
#         myuser.is_active=False
#
#         myuser.save()
#         messages.success(request,"account created successfully")
#         #welcome
#         subject = "Welcome to Obsessed Programmers"
#         message = f"Hello {myuser.first_name},\n\n"\
#           "We are thrilled to welcome you to Obsessed Programmers!\n\n"\
#           "Thank you for joining our community. To get started, please confirm your email.\n\n"\
#           "Best regards,\n"\
#           "The Obsessed Programmers Team"
#
#         #conformation email
#         current_site=get_current_site(request)
#         email_subject="confirm your email"
#         message2=render_to_string('email_confirmation.html',{
#             'name':myuser.first_name,
#             'domain':current_site.domain,
#             'uid':urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token':generate_token.make_token(myuser),
#         })
#         email=EmailMessage(
#             email_subject,
#             message2,
#             settings.EMAIL_HOST_USER,
#             [myuser.email]
#         )
#         email.fail_silently=True
#         email.send()
#
#         from_email=settings.EMAIL_HOST_USER
#         to_list=[myuser.email]
#         send_mail(subject,message,from_email,to_list,fail_silently=True)
#
#
#         return redirect('signin')
#     return render(request,'authentication/signup.html')

# def signin_view(request):

#     if request.method=="POST":
#         username=request.POST['username']
#         pass1=request.POST['pass1']
#         user=authenticate(username=username,password=pass1)
#         if user is not None:
#             login(request,user)
#             fname=user.first_name
#             messages.success(request,"Logging successfull..")
#             return home(request)
#         else:
#             messages.error(request,"please signup......")
#             return redirect('signin')

#     return render(request, 'authentication/signin.html')
from django.urls import reverse
from qr_code_authentication_app.models import Profile
# def signin_view(request):
#
#
#
#     if not request.user.is_authenticated:
#         if request.method == "POST":
#             username = request.POST.get('username')
#             password = request.POST.get('pass1')
#             user = authenticate(request, username=username, password=password)
#             if user is not None:
#                 # login(request, user)
#                 # messages.success(request, "Login successful.")
#                 print("signin_view :", username)
#                 print("user authenticated :",request.user.is_authenticated)
#                 profile = Profile.objects.get(user=request.user)
#                 qr_auth = profile.qr_auth
#                 if qr_auth==True:
#
#                     print(qr_auth*50)
#                     return redirect(reverse('login',kwargs={'username': username}))  # Assuming 'home' is the name of your home URL
#                 else:
#                     login(request, user)
#                     messages.success(request, "Login successful.")
#                     return redirect(reverse(home))
#
#             else:
#
#
#                 messages.error(request, "Invalid username or password.")
#
#                 return redirect(reverse('signin',))  # Redirect back to signin page
#         return render(request, 'authentication/signin.html')
#     else:
#         return render(request, 'authentication/home.html')
from qr_code_authentication_app.views import qr_login
def signin_view(request):

    if not request.user.is_authenticated:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('pass1')
            user = authenticate(request, username=username, password=password)

            if user is not None :

                if user.profile.qr_auth:  # Check if QR authentication is enabled for the user

                    request.session['username'] = username
                    return redirect(reverse('login'))

                else:
                    login(request, user)
                    messages.success(request, "Login successful.")
                    return redirect(reverse('home'))
            else:
                messages.error(request, "Invalid username or password.")
                return redirect(reverse('signin'))
        return render(request, 'authentication/signin.html')
    else:
        return home(request)

from django.contrib.auth import logout
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse

def signout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect(reverse('signin'))


def activate(request,uid64,token):
    try:
        uid=force_str(urlsafe_base64_decode(uid64))
        myuser=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser=None
    if myuser is not None and generate_token.check_token(myuser,token):
        myuser.is_active=True
        myuser.save()
        fname=myuser.first_name
        # login(request,myuser)
        # return redirect('home')
        messages.success(request, 'Account is activated signin Now !!.')
        # return render(request, 'authentication/home.html',{'fname':fname})
        return redirect(reverse('signin'))
    else:

        return(request,'activation_failed.html')






from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from qr_code_authentication_app.models import Profile


@login_required
def qr_auth_function(request):
    # Retrieve the current user
    user = request.user
    # Access the profile associated with the user
    try:
        # Access the profile associated with the user
        profile = user.profile
    except Profile.DoesNotExist:
        # If profile does not exist, create a new one
        return redirect(reverse('register'))

    print("qr auth fun : ", profile.qr_auth)
    if profile.qr_auth is False:
        print("qr auth fun : ",profile.qr_auth)
        # Toggle the qr_auth attribute
        profile.qr_auth = True
        # Save the profile to update the changes
        profile.save()

        print("qr auth fun in if: ", profile.qr_auth)
        return redirect(reverse('register'))
    else:
        profile.qr_auth = False
        # Save the profile to update the changes
        profile.save()

        print("qr auth fun in if: ", profile.qr_auth)
        return redirect(reverse('home',))


    # Return a JSON response indicating the new status of qr_auth
    return redirect(reverse('home'))






















#forgot passward

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import PasswordResetToken
from .forms import ForgotPasswordForm, ResetPasswordForm
from django.utils.encoding import force_str

from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import update_session_auth_hash

def forgot_password(request):
    if request.method == 'POST':
        form = ForgotPasswordForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                user = None

            if user:
                # Generate and store password reset token
                token = default_token_generator.make_token(user)
                PasswordResetToken.objects.create(user=user, token=token, created_at=timezone.now())

                # Send password reset email
                reset_link = request.build_absolute_uri('/reset-password/') + token + '/'
                send_mail(
                    'Reset Your Password',
                    f'Click the following link to reset your password: {reset_link}',
                    settings.EMAIL_HOST_USER,
                    [email],
                    fail_silently=False,
                )
                messages.success(request, 'Password reset email sent. Please check your email.')
            else:
                messages.error(request, 'No user found with that email address.')
            return redirect('forgot-password')
    else:
        form = ForgotPasswordForm()
    return render(request, 'forgot_password.html', {'form': form})

def reset_password(request, token):
    try:
        password_reset_token = PasswordResetToken.objects.get(token=token)
    except PasswordResetToken.DoesNotExist:
        messages.error(request, 'Invalid password reset link.')
        return redirect('forgot-password')

    if request.method == 'POST':
        form = ResetPasswordForm(request.POST)
        if form.is_valid():
            new_password = form.cleaned_data['new_password']
            user = password_reset_token.user
            user.set_password(new_password)
            user.save()

            # Delete the password reset token
            password_reset_token.delete()

            # Update user's session authentication hash
            update_session_auth_hash(request, user)

            messages.success(request, 'Password reset successful. You can now login with your new password.')
            return redirect('login')
    else:
        form = ResetPasswordForm()
    return render(request, 'reset_password.html', {'form': form})


# from django.shortcuts import render, redirect, reverse
# from django.contrib import messages
# from django.contrib.auth import authenticate, login
# from django.contrib.auth.models import User
# from django.core.mail import EmailMessage, send_mail
# from django.contrib.sites.shortcuts import get_current_site
# from django.template.loader import render_to_string
# from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
# from django.utils.encoding import force_bytes
# from .tokens import generate_token
# from qr_code_authentication_app.models import Profile
# from django.conf import settings
#
#
# def signup_view(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         fname = request.POST['fname']
#         lname = request.POST['lname']
#         email = request.POST['email']
#         pass1 = request.POST['pass1']
#         pass2 = request.POST['pass2']
#         digit = len(pass1)
#
#         if digit <= 8:
#             messages.error(request, "Password should be greater than 8 characters.")
#             context = {'username': username, 'fname': fname, 'lname': lname, 'email': email}
#             return render(request, 'authentication/signup.html', context)
#         elif pass1 != pass2:
#             messages.error(request, "Passwords do not match.")
#             context = {'username': username, 'fname': fname, 'lname': lname, 'email': email}
#             return render(request, 'authentication/signup.html', context)
#
#         if User.objects.filter(username=username).exists():
#             messages.error(request, "Username already exists.")
#             return redirect("home")
#
#         if User.objects.filter(email=email).exists():
#             messages.error(request, "Email already exists.")
#             return redirect("home")
#
#         myuser = User.objects.create_user(username, email, pass1)
#         myuser.first_name = fname
#         myuser.last_name = lname
#         myuser.is_active = False
#         myuser.save()
#
#         # Create a Profile for the new user
#         Profile.objects.create(user=myuser)
#
#         messages.success(request, "Account created successfully.")
#
#         # Send welcome email
#         subject = "Welcome to Obsessed Programmers"
#         message = f"Hello {myuser.first_name},\n\n" \
#                   "We are thrilled to welcome you to Obsessed Programmers!\n\n" \
#                   "Thank you for joining our community. To get started, please confirm your email.\n\n" \
#                   "Best regards,\n" \
#                   "The Obsessed Programmers Team"
#
#         from_email = settings.EMAIL_HOST_USER
#         to_list = [myuser.email]
#         send_mail(subject, message, from_email, to_list, fail_silently=True)
#
#         # Send confirmation email
#         current_site = get_current_site(request)
#         email_subject = "Confirm your email"
#         message2 = render_to_string('email_confirmation.html', {
#             'name': myuser.first_name,
#             'domain': current_site.domain,
#             'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
#             'token': generate_token.make_token(myuser),
#         })
#         email = EmailMessage(
#             email_subject,
#             message2,
#             from_email,
#             [myuser.email]
#         )
#         email.fail_silently = True
#         email.send()
#
#         return redirect('signin')
#     return render(request, 'authentication/signup.html')

from django.shortcuts import render, redirect, reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.core.mail import EmailMessage, send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from .tokens import generate_token
from qr_code_authentication_app.models import Profile
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

def signup_view(request):
    if request.method == "POST":
        username = request.POST.get('username')
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        digit = len(pass1)

        context = {'username': username, 'fname': fname, 'lname': lname, 'email': email}

        if digit <= 8:
            messages.error(request, "Password should be greater than 8 characters.")
            return render(request, 'authentication/signup.html', context)
        elif pass1 != pass2:
            messages.error(request, "Passwords do not match.")
            return render(request, 'authentication/signup.html', context)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("home")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists.")
            return redirect("home")

        try:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.first_name = fname
            myuser.last_name = lname
            myuser.is_active = False
            myuser.save()

            # Create a Profile for the new user
            Profile.objects.create(user=myuser)



            # Send welcome email
            subject = "Welcome to E-authentication"
            message = f"Hello {myuser.first_name},\n\n" \
                      "We are thrilled to welcome you to E-authentication!\n\n" \
                      "Thank you for joining our community. To get started, please confirm your email.\n\n" \
                      "Best regards,\n" \
                      "The E-Authentication Team"

            from_email = settings.EMAIL_HOST_USER
            to_list = [myuser.email]
            try:
                send_mail(subject, message, from_email, to_list, fail_silently=False)
                messages.success(request, "Account created successfully. Check Your Email Box To Activate Account !!! ")
            except Exception as e:
                messages.error(request, "Failed to send email !!! , Check Internet connection ")
                logger.error(f"Failed to send welcome email to {myuser.email}: {e}")

            # Send confirmation email
            current_site = get_current_site(request)
            email_subject = "Confirm your email"
            message2 = render_to_string('email_confirmation.html', {
                'name': myuser.first_name,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
                'token': generate_token.make_token(myuser),
            })
            email = EmailMessage(
                email_subject,
                message2,
                from_email,
                [myuser.email]
            )
            try:
                email.send(fail_silently=False)
            except Exception as e:
                print("deleting user not send email check net connection")
                myuser.delete()
                logger.error(f"Failed to send confirmation email to {myuser.email}: {e}")

            return redirect('signin')
        except Exception as e:
            logger.error(f"An error occurred during signup: {e}")
            messages.error(request, "An unexpected error occurred. Please try again.")
            return render(request, 'authentication/signup.html', context)

    return render(request, 'authentication/signup.html')

