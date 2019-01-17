from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class Signup_Form(UserCreationForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Username"}))
    email = forms.EmailField(max_length=200, help_text='Required', widget=forms.TextInput(attrs={"placeholder": "Email"}))
    password1 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Password"}))
    password2 = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder": "Confirm Password"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_username(self, *args, **kwargs):
        username = self.cleaned_data.get("username")

        if len(str(username)) >= 20:
            raise forms.ValidationError("Username should be under 20 characters long")
        if " " in username:
            raise forms.ValidationError("Username can't contain spaces")
        else:
            return username
        
    def clean_email(self, *args, **kwargs):
        email = self.cleaned_data.get("email")

        try:
            match = User.objects.get(email = email)
            raise forms.ValidationError("This email address is already in use")
        except User.DoesNotExist:
            return email

    def clean_password(self, *args, **kwargs):
        password1 = self.cleaned_data.get("password1")
        if " " in password1:
            raise forms.ValidationError("password can't contain spaces")
        else:
            return password1
        

class startsub_form(forms.Form):
    startsub = forms.IntegerField(widget=forms.HiddenInput())

    class Meta:
        fields=['startsub',]

