from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, SetPasswordForm
from django import forms
from .models import Profile


class UserInfoFom(forms.ModelForm):
    phone = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Phone'}), required=False)
    address1 =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address1'}), required=False)
    address2 =  forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Address2'}), required=False)
    city = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'city'}), required=False)
    state = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'State'}), required=False)
    zipcode = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Zipcode'}), required=False)
    country = forms.CharField(label="", widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Country'}), required=False)

    class Meta:
        model = Profile
        fields = ('phone', 'address1', 'address2', 'city', 'state', 'zipcode', 'country',)


class ChangePasswordForm(SetPasswordForm):
    class Meta:
        model = User
        fields = ['new_password1', 'new_password2']
    
    new_password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'Please enter more than 8 characters'
            }
        )
    )
    new_password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'Please re-enter your password'
            }
        )
    )

class UpdateUserForm(UserChangeForm):
    #hide password
    password = None
    #Get other fields

    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your username:'})
    )
    
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your name:'})
    )
    last_name = forms.CharField(
       label="",
       max_length=50,
       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your family:'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your email:'})
    )

    class Meta:
        model = User
        fields = ('username','first_name','last_name','email')

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(
        label="",
        max_length=50,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your name:'})
    )
    last_name = forms.CharField(
       label="",
       max_length=50,
       widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your family:'})
    )
    email = forms.EmailField(
        label="",
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your email:'})
    )
    username = forms.CharField(
        label="",
        max_length=20,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'Please enter your username:'})
    )
    password1 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'Please enter more than 8 characters'
            }
        )
    )
    password2 = forms.CharField(
        label="",
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control',
                'name':'password',
                'type':'password',
                'placeholder':'Please re-enter your password'
            }
        )
    )
    class Meta:
        model = User
        fields = ('first_name','last_name','email','username','password1','password2')