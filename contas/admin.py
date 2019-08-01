# from django.contrib import admin

# from contas.models import Usuario, GerenteConta

# # # Register your models here.

# admin.site.register(Usuario)
# admin.site.register(GerenteConta)

from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import SolicitanteCreationForm, SolicitanteChangeForm, SuporteContaCreationForm, SuporteContaChangeForm, AdministradorCreationForm, AdministradorChangeForm
from .models import SuporteConta, Administrador, Solicitante, TipoSolicitante

class SolicitanteAdmin(UserAdmin):
    add_form = SolicitanteCreationForm
    form = SolicitanteChangeForm
    model = Solicitante
    list_display = ['username', 'first_name','email','telefone']

    fieldsets = (
		(None, {'fields': ('username', 'email', 'password')}),
		('Outras Informações', {'fields': ('first_name', 'last_name', 'telefone', 'foto')}),
		('Permissões', {'fields': ('is_active','tipo_solicitante','curso_setor')}),
		# ('Permissões', {'fields': ('is_superuser', 'is_staff', 'is_active',)}),
	)


class SuporteContaAdmin(UserAdmin):
    add_form = SuporteContaCreationForm
    form = SuporteContaChangeForm
    model = SuporteConta
    list_display = ['username', 'first_name','email','telefone']

    fieldsets = (
		(None, {'fields': ('username', 'email', 'password')}),
		('Outras Informações', {'fields': ('first_name', 'last_name', 'telefone', 'foto')}),
		('Permissões', {'fields': ('is_active',)}),
		# ('Permissões', {'fields': ('tipo_conta','is_superuser', 'is_staff', 'is_active',)}),
	)


class AdministradorAdmin(UserAdmin):
    add_form = AdministradorCreationForm
    form = AdministradorChangeForm
    model = Administrador
    list_display = ['username', 'first_name','email','telefone']

    fieldsets = (
		(None, {'fields': ('username', 'email', 'password')}),
		('Outras Informações', {'fields': ('first_name', 'last_name', 'telefone', 'foto')}),
		('Permissões', {'fields': ('is_active',)}),
		# ('Permissões', {'fields': ('tipo_conta','is_superuser', 'is_staff', 'is_active',)}),
	)

admin.site.register(Solicitante, SolicitanteAdmin)
admin.site.register(SuporteConta, SuporteContaAdmin)
admin.site.register(Administrador, AdministradorAdmin)
admin.site.register(TipoSolicitante)