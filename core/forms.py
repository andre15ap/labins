from django import forms
from django.contrib.auth.forms import AuthenticationForm
from contas.models import Usuario


class LoginForm(AuthenticationForm):
	username = forms.CharField(label='CPF',widget=forms.TextInput(attrs={'class':'form-control','placeholder':'CPF sem pontos ou traços'}))
	password = forms.CharField(label='Senha',widget=forms.PasswordInput(attrs={'class':'form-control','placeholder':'Digite sua senha'}))
