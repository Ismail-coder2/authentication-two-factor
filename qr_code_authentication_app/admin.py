from django.contrib import admin
from .models import Profile

# Register the Profile model with the admin site
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Define the fields to be displayed in the admin interface
    list_display = ['user','qr_auth']

    # Optionally, you can customize the admin form fields
    # by specifying the fields attribute:
    # fields = ['user', 'otp_secret', 'qr_auth']

    # Or exclude some fields if needed:
    exclude = ['otp_secret']
