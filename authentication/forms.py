from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.utils.translation import gettext_lazy as _


from authentication.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'role', 'responsible')

class UpdateUserForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'email', 'profile_picture', 'address')


class LoginForm(forms.Form):
    email = forms.EmailField(label=_('Adresse email'), required=True)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput, label=_('Mot de passe'), required=True)

