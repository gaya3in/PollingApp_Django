from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import RegexValidator
from django.forms import ModelForm
from .models import Poll


class RegisterForm(UserCreationForm):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone = forms.CharField(validators=[phone_regex], max_length=17)
    class Meta:
        model = User
        fields = ['username','email', 'password1', 'password2', 'phone']

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50)
    password = forms.CharField(widget = forms.PasswordInput())


class VotingForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question','option_1','option_2','option_3', 'option_4']

class CreatePollForm(ModelForm):
    class Meta:
        model = Poll
        fields = ['question','option_1','option_2','option_3', 'option_4']

        widget =  {
            'question': forms.Textarea(attrs={'class': 'form-control', 'row': 3}),
            'option_1': forms.TextInput(attrs={'class': 'form-control'}),
            'option_2': forms.TextInput(attrs={'class': 'form-control'}),
            'option_3': forms.TextInput(attrs={'class': 'form-control'}),
            'option_4': forms.TextInput(attrs={'class': 'form-control'})
        }
