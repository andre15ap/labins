from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from .models import SuporteConta, Administrador, Solicitante, TipoSolicitante, Usuario

# class UsuarioCreationForm(UserCreationForm):
#     class Meta(UserCreationForm.Meta):
#         model = Usuario
#         fields = ('username', 'email', 'telefone')

# class UsuarioChangeForm(UserChangeForm):

#     class Meta:
#         model = Usuario
#         fields = ('username', 'email', 'telefone')

# encoding: utf-8
import re

def valida_cpf(cpf=''):
    if not cpf.isdigit():
        return False
    cpf = cpf.replace('.', '').replace('-', '')
    if len(cpf) != 11:
        return False
    i = d1 = d2 = 0
    if cpf in ['11111111111', '22222222222', '33333333333', '44444444444', '55555555555', '66666666666', '77777777777', '88888888888', '99999999999']:
        return False
    while i < 10:
        d1, d2, i = (d1 + (int(cpf[i]) * (11 - i - 1))) % 11 if i < 9 else d1, (d2 + (int(cpf[i]) * (11-i))) % 11, i + 1
    return (int(cpf[9]) == (11-d1 if d1 > 1 else 0)) and (int(cpf[10]) == (11 - d2 if d2 > 1 else 0))


class SolicitanteCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Solicitante
        fields = (
            'username','password1','password2', 'first_name', 'last_name', 'email', 'telefone', 'foto','curso_setor', 'tipo_solicitante'
            )
        labels = ({
                    'username' : 'CPF', 
                    'tipo_solicitante' : 'Tipo de Conta',
                    'curso_setor' : 'Curso ou Setor'
                })
    
    def __init__(self, *args, **kwargs):
        super(SolicitanteCreationForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget.attrs = {'class': 'form-control','placeholder':'digite seu CPF sem pontos ou traços'}
        self.fields['password1'].widget.attrs = {'class': 'form-control','placeholder':'digite senha'}
        self.fields['password2'].widget.attrs = {'class': 'form-control', 'placeholder':'confirme senha'}
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'placeholder':'primeiro nome'}
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'placeholder':'restante do nome'}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder':'digite seu email'}
        self.fields['telefone'].widget.attrs = {'class': 'form-control', 'placeholder':'digite seu telefone'}
        self.fields['foto'].widget.attrs = {'class': 'form-control-file'}
        self.fields['tipo_solicitante'].widget.attrs = {'class': 'form-control'}
        self.fields['curso_setor'].widget.attrs = {'class': 'form-control'}




    def clean_username(self):
        username = self.cleaned_data.get('username')
        if username:
            username = re.sub('[^0-9]', '', username)
        if not valida_cpf(username):
            raise forms.ValidationError('CPF inválido')
		
        if Usuario.objects.filter(username=username).exists():
            raise forms.ValidationError('CPF Já cadastrado')
        return username


class SolicitanteChangeForm(UserChangeForm):
    class Meta:
        model = Solicitante
        fields = ('username', 'email', 'telefone')


class SuporteContaCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = SuporteConta
        fields = ('username', 'email', 'telefone')

class SuporteContaChangeForm(UserChangeForm):
    class Meta:
        model = SuporteConta
        fields = ('username', 'email', 'telefone')

class AdministradorCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Administrador
        fields = ('username', 'email', 'telefone')

class AdministradorChangeForm(UserChangeForm):
    class Meta:
        model = Administrador
        fields = ('username', 'email', 'telefone')

class TipoSolicitanteForm(forms.ModelForm):
    class Meta:
        model = TipoSolicitante
        fields = ('tipo', 'descricao') 

    def __init__(self, *args, **kwargs):
        super(TipoSolicitanteForm, self).__init__(*args, **kwargs)
        self.fields['tipo'].widget.attrs = {'class': 'form-control','placeholder':'Nome do tipo solicitante'}
        self.fields['descricao'].widget.attrs = {'class': 'form-control','rows': 3, 'cols': 40, 'style':'resize:none','placeholder':'Descrição do tipo de solicitante'}

class SuporteAtualizarDadosForm(forms.ModelForm):
    class Meta:
        model = SuporteConta
        fields = ('first_name', 'last_name', 'telefone', 'email', 'foto')

    def __init__(self, *args, **kwargs):
        super(SuporteAtualizarDadosForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'placeholder':'primeiro nome', 'required':True}
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'placeholder':'restante do nome', 'required':True}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder':'digite seu email', 'required':True}
        self.fields['telefone'].widget.attrs = {'class': 'form-control', 'placeholder':'digite seu telefone', 'required':True}
        self.fields['foto'].widget.attrs = {'class': 'form-control-file'}
        
        
class SolicitanteAtualizarDadosForm(forms.ModelForm):
    class Meta:
        model = Solicitante
        fields = ('first_name', 'last_name', 'telefone', 'email', 'foto', 'curso_setor')
    
    def __init__(self, *args, **kwargs):
        super(SolicitanteAtualizarDadosForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs = {'class': 'form-control', 'placeholder':'primeiro nome', 'required':True}
        self.fields['last_name'].widget.attrs = {'class': 'form-control', 'placeholder':'restante do nome', 'required':True}
        self.fields['email'].widget.attrs = {'class': 'form-control', 'placeholder':'digite seu email', 'required':True}
        self.fields['telefone'].widget.attrs = {'class': 'form-control', 'placeholder':'digite seu telefone', 'required':True}
        self.fields['foto'].widget.attrs = {'class': 'form-control-file'}
        self.fields['curso_setor'].widget.attrs = {'class': 'form-control', 'required':True}

class TrocarSenhaForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(TrocarSenhaForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })



class RecuperarSenhaForm(forms.Form):
    cpf = forms.CharField(label='CPF')
    email = forms.EmailField(label='Email')
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirme a senha', widget=forms.PasswordInput)
    valor_cpf = None
   
 
    def __init__(self, *args, **kwargs):
        super(RecuperarSenhaForm, self).__init__(*args, **kwargs)
        self.fields['cpf'].widget.attrs = {'class': 'form-control','placeholder':'digite seu CPF sem pontos ou traços', 'required':True}
        self.fields['email'].widget.attrs = {'class': 'form-control','placeholder':'digite seu email utilizado no cadastro', 'required':True}
        self.fields['password'].widget.attrs = {'class': 'form-control','placeholder':'digite a nova senha', 'required':True}
        self.fields['password2'].widget.attrs = {'class': 'form-control','placeholder':'confirme a senha', 'required':True}

    def clean_cpf(self):
        cpf = self.cleaned_data.get("cpf")
        self.valor_cpf = cpf
        usuario_exist = Usuario.objects.filter(username=cpf).exists()
        if not usuario_exist:
            raise forms.ValidationError('CPF Não encontrado')
        
        if Usuario.objects.filter(username=cpf, is_active=False).exists():
            raise forms.ValidationError('Usuario Aguardando Liberação, entre em contato com algum suporte de conta')
        return cpf

    def clean_email(self):
        email = self.cleaned_data.get("email")

        email_certo = Usuario.objects.filter(username=self.valor_cpf, email=email).exists()

        if not email_certo:
            raise forms.ValidationError('Email Não corresponde ao cadastrado')
        return email

    def clean_password(self):
        password = self.cleaned_data.get("password")        
       
        if len(password) < 8:
            raise forms.ValidationError('Senhas Muito curta, deve ter no minimo 8 caracteres')
        return password


    def clean_password2(self):
        
        password = self.cleaned_data.get("password")
        password2 = self.cleaned_data.get("password2")
        # self.fields['password2'].widget.attrs = {'class' :'form-control is-invalid','placeholder':'confirme a senha'}
        if password and password2 and password != password2:
            raise forms.ValidationError('Senhas não conferem')
        return password2