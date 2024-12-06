from django import forms
from django.contrib.auth import get_user_model
from .models import Profile

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)



class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        label='Password',
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label='Password confirmation',
        widget=forms.PasswordInput
    )

    class Meta:
        model = get_user_model()
        fields = ('username', 'email', 'first_name')

    def clean_password2(self: forms.Form) -> str:
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError('Email already in use.')
        return data



class UserEditForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email')

    # def clean_email(self):
    #     data = self.cleaned_data['email']
    #     qs = User.objects.exclude(
    #         id=self.instance.exclude.id
    #     ).filter(
    #         email=data
    #     )
    #     if qs.exists():
    #         raise forms.ValidationError('Email already in use.')
    #     return data
    def clean_email(self):
        email = self.cleaned_data['email']
        # Check if the email is already in use by another user
        users_with_email = User.objects.filter(email=email).exclude(pk=self.instance.pk)
        if users_with_email.exists():
            raise forms.ValidationError('A user with this email already exists.')
        return email



class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('date_of_birth', 'photo')