from django import forms

class ForgotPasswordForm(forms.Form):
    # email = forms.EmailField(label='')
    email = forms.EmailField(label='', widget=forms.EmailInput(attrs={'class': 'form-control','placeholder': 'Email Address'}))

class ResetPasswordForm(forms.Form):
    new_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'New Password'}))
    confirm_password = forms.CharField(label='', widget=forms.PasswordInput(attrs={'class': 'form-control','placeholder': 'Confirm Password'}))

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')
        if new_password != confirm_password:
            raise forms.ValidationError("Passwords do not match.")
        return cleaned_data
