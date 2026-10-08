from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'form-control',
        'placeholder': 'Email address',
    }))
    full_name = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Full Name',
    }))
    referral_code = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Referral Code (Optional)',
    }))
    username = forms.CharField(max_length=150, required=True, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Username',
    }))
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Password',
    }))
    password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput(attrs={
        'class': 'form-control',
        'placeholder': 'Confirm Password',
    }))

    class Meta:
        model = User
        fields = ('username', 'email', 'full_name', 'referral_code', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            UserProfile.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                referral_code=self.cleaned_data.get('referral_code', '')
            )
        return user 