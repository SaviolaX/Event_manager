from django import forms
from django.contrib.auth.models import User

from .models import Profile


class UserRegistrationForm(forms.ModelForm):
    """Form for user registration"""
    password = forms.CharField(label='Password',
                               widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password',
                                widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'email')

    def clean_password2(self):
        """Compare password1 and password2"""
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password don\'t match.')
        return cd['password2']


class EditProfileForm(forms.ModelForm):
    """Edit form for profile"""
    class Meta:
        model = Profile
        fields = ('city', 'photo')


class EditUserForm(forms.ModelForm):
    """Edit form for user"""
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email')
