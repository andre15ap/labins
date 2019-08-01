from django.shortcuts import render

from django.views.generic import View, TemplateView, CreateView, ListView, DetailView, UpdateView, DeleteView

# from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.contrib import messages
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth import update_session_auth_hash

import json

from .models import Solicitante, Usuario, SuporteConta, TipoSolicitante
from atividades.models import Atividade, TurmaAtividade, Reserva
from .forms import SolicitanteCreationForm, TipoSolicitanteForm, SolicitanteChangeForm
from .forms import SuporteAtualizarDadosForm, SolicitanteAtualizarDadosForm, TrocarSenhaForm

# Create your views here.

class HomeView(LoginRequiredMixin, View):
    def get(self, request):
        suporte = SuporteConta.objects.filter(id=request.user.id).count()
        if suporte == 1:
        	return HttpResponse('contas/index.html')
        return HttpResponse('<h1>nao e suporte</h1>')


# PRIMEIRA VIEW CHAMADA, ESCOLHE SE É SUPORTE OU SOLICITANTE
class IndexListView(LoginRequiredMixin, ListView):
	template_name = 'contas/index_solicitante.html'
	#MUDA O QUERYSET DE ACORDO COM O TIPO DE USUÁRIO
	def get_queryset(self):
		#FUNCOES PARA DESATIVAR TURMAS E RESERVAS PASSADAS
		Reserva.desativar_auto()
		TurmaAtividade.desativar_auto()
		user = self.request.user
		lista = []
		#FUNÇÃO PARA VER SE O USUARIO É SUPORTE OU SOLICITANTE
		if user.permissao_suporte():
			lista = TurmaAtividade.objects.filter(ativo=True,responsavel=user)
		else:
			lista = Atividade.objects.filter(ativo=True,solicitante=user)
		return lista

	#VERIFICA SE É SUPORTE MUDA O CONTEXT E O TEMPLATE
	def get_context_data(self, **kwargs):
		context = super(IndexListView, self).get_context_data(**kwargs)
		if context['view'].request.user.permissao_suporte():
			self.template_name = 'contas/index_suporte.html'
			bloqueadas = TurmaAtividade.objects.filter(ativo=True,responsavel=context['view'].request.user, status=TurmaAtividade.BLOQUEADA)
			sem_responsavel = TurmaAtividade.objects.filter(ativo = True, responsavel=None)
			atividades_inativas = Atividade.objects.filter(ativo=True, liberada=False)
			suportes = SuporteConta.objects.filter(ativo=True)
			solicitantes = Solicitante.objects.filter(ativo=True, is_active=False)
			context	['turma_sem_responsavel_list'] = sem_responsavel
			context['atividades_inativas_list'] = atividades_inativas
			context['suporte_list'] = suportes
			context['solicitante_list'] = solicitantes
			context['bloqueada_list'] = bloqueadas

		return context


	def set_suporte(self):
		self.template_name = 'contas/index_suporte.html'


class SolicitanteCreateView(CreateView):
    template_name = "contas/registrar.html"
    model = Solicitante
    form_class = SolicitanteCreationForm
    success_url = reverse_lazy("contas:index")

    def form_valid(self, form):
    	solicitante = form.save(commit=False)
    	solicitante.is_active = False
    	solicitante.save()
    	messages.add_message(self.request, messages.SUCCESS, 'Cadastro Relizado com sucesso! Aguarde seu cadastro ser analizado')
    	return HttpResponseRedirect(self.success_url)



class SolicitanteListView(LoginRequiredMixin, ListView):
    model = Solicitante
    template_name = "contas/solicitante_list.html"


class SolicitanteDetailView(LoginRequiredMixin, DetailView):
    model = Solicitante
    template_name = "contas/solicitante_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SolicitanteDetailView, self).get_context_data(**kwargs)
        solicitante = context['solicitante']
        atividades = Atividade.objects.filter(solicitante__id=solicitante.id)
        turmas = TurmaAtividade.objects.filter(atividade__solicitante__id=solicitante.id)
        context['atividade_list'] = atividades
        context['turma_list'] = turmas
        return context

class UsuarioView(LoginRequiredMixin, View):
    def get(self, request):
        user = request.user

        if user.permissao_suporte():
            usuario = SuporteConta.objects.get(id=user.id)
        else:
            usuario = Solicitante.objects.get(id=user.id)
        context = {
            'usuario' : usuario
        }
        return render(request, 'contas/usuario_detail.html', context)

class SuporteDetailView(LoginRequiredMixin, DetailView):
    model = SuporteConta
    context_object_name = 'suporte'
    template_name = "contas/suporte_detail.html"

    def get_context_data(self, **kwargs):
        context = super(SuporteDetailView, self).get_context_data(**kwargs)

        pk = self.object.pk
        turmas = TurmaAtividade.objects.filter(responsavel__id=pk)
        context['turma_list'] = turmas
        return context

class SuporteAtualizarDadosView(LoginRequiredMixin, UpdateView):
	form_class = SuporteAtualizarDadosForm
	model = SuporteConta
	template_name = 'contas/forms/usuario_atualizar_dados.html'
	success_url = reverse_lazy("contas:usuario_detail")

class SolicitanteAtualizarDadosView(LoginRequiredMixin, UpdateView):
	form_class = SolicitanteAtualizarDadosForm
	model = Solicitante
	template_name = 'contas/forms/usuario_atualizar_dados.html'
	success_url = reverse_lazy("contas:usuario_detail")


class AlterarSenhaView(LoginRequiredMixin, PasswordChangeView):
	template_name = 'contas/forms/trocar_senha.html'
	success_url = reverse_lazy('contas:usuario_detail')
	form_class = TrocarSenhaForm

	def form_valid(self, form):
		form.save()
		messages.add_message(self.request, messages.SUCCESS, 'Senha Alterada com sucesso!')
		#PARA MANTER USUARIO LOGADO NA SESSION
		update_session_auth_hash(self.request, form.user)
		return super(PasswordChangeView, self).form_valid(form)


class SolicitanteLiberaAjax(LoginRequiredMixin, View):
	def get(self, request, pk):
		solicitante = Solicitante.objects.get(id=pk)
		user = request.user
		if user.permissao_suporte():
			solicitante.is_active = True
			solicitante.save()

		resultado = {}

		resultado['liberou'] = True
		resultado['nova_situacao'] = solicitante.is_active

		return HttpResponse(json.dumps(resultado), content_type="application/json")

class SolicitanteDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE ATIVIDADE ATIVAS QUE PERTENCAM AO SOLICITANTE
		solicitante = Solicitante.objects.get(id=pk)
		resultado = solicitante.dependencia()
		if not resultado['dependencia_atividade']:
			solicitante.ativo = False
			solicitante.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")

class LstarTurmasAjax(LoginRequiredMixin, View):
	def get(self, request, pk):
		# print(request)
		turmas = TurmaAtividade.objects.filter(atividade__id=pk)

		turma_list = []

		for turma in turmas:
			campos = {}
			campos['id'] = str(turma.id)
			campos['nome'] = turma.nome
			responsavel = turma.responsavel
			if not responsavel:
				responsavel = 'Sem Responsável'
			campos['responsavel'] = str(responsavel)
			momento = turma.momento
			if not momento:
				momento = 'Sem Momento'
			campos['momento'] = str(momento)
			campos['status'] = str(turma.status)
			turma_list.append(campos)

		return HttpResponse(json.dumps(turma_list), content_type="application/json")

####################### INICIO CRUD TIPO SOLICITANTE ##########################################
class TipoSolicitanteCreateView(LoginRequiredMixin, CreateView):
    template_name = "contas/forms/gerencia/tipo_solicitante_form.html"
    model = TipoSolicitante
    form_class = TipoSolicitanteForm
    success_url = reverse_lazy("contas:listar_tipo_solicitante")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	tipo_solicitante = form.save(commit=False)
    	if self.request.user.permissao_suporte():
    		tipo_solicitante.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Tipo de Solicitante Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Tipo de Solicitante')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class TipoSolicitanteUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "contas/forms/gerencia/tipo_solicitante_form.html"
    model = TipoSolicitante
    form_class = TipoSolicitanteForm
    success_url = reverse_lazy("contas:listar_tipo_solicitante")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	tipo_solicitante = form.save(commit=False)
    	if self.request.user.permissao_suporte():
            dependencia = tipo_solicitante.dependencia()
            if dependencia['dependencia_solicitante']:
                lista = ''
                for dep in dependencia['solicitante_list']:
                    lista += ' Solicitante: {}.'.format(dep['solicitante'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias Ativas, {}'.format(lista))
            else:
                tipo_solicitante.save()
                messages.add_message(self.request, messages.SUCCESS, 'Tipo de Solicitante Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Tipo de Solicitante')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class TipoSolicitanteListView(ListView):
    model = TipoSolicitante
    template_name = "contas/gerencia/tipo_solicitante_list.html"

class TipoSolicitanteDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE SOLICITANTES ATIVOS QUE PERTENCAM AO TIPO SOLICITANTE
		tipo_solicitante = TipoSolicitante.objects.get(id=pk)
		resultado = tipo_solicitante.dependencia()
		if not resultado['dependencia_solicitante']:
			tipo_solicitante.ativo = False
			tipo_solicitante.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


####################### FIM CRUD TIPO SOLICITANTE ##########################################

from .forms import RecuperarSenhaForm
class RecupararSenhaView(View):
	template_name = 'contas/forms/recuperar_senha.html'
	form_class = RecuperarSenhaForm
	success_url = reverse_lazy("contas:index")
	
	def get(self, request, **kwargs):
		context = {
			'form' : self.form_class
		}
		return render(request, self.template_name, context)
	
	def post(self, request, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			cpf = form.cleaned_data['cpf']
			senha1 = form.cleaned_data['password']
			senha2 = form.cleaned_data['password2']
			email = form.cleaned_data['email']
			if senha1 == senha1:
				try:
					solicitante = Usuario.objects.get(username=cpf, email=email)
					solicitante.set_password(senha1)
					solicitante.save()
					messages.add_message(self.request, messages.SUCCESS, 'Senha Alterado com sucesso!')
				except:
					messages.add_message(self.request, messages.ERROR, 'Algo deu errado!')
				
				return HttpResponseRedirect(self.success_url)
				
			else:
				print('senhas não conferem')
		else:
			
			messages.add_message(self.request, messages.ERROR, 'Formulario inválido!')
		
		context = {
			'form' : form
		}
		return render(request, self.template_name, context)
