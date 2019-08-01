from django.shortcuts import render

from django.views.generic import View, TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from django.http import JsonResponse
from django.template.loader import render_to_string
import json

from django.core.exceptions import PermissionDenied
from datetime import date
from datetime import datetime



from .forms import AtividadeForm, SistemaOperacionalForm, TipoAtividadeForm, SoftwareForm,TurmaAtividadeForm 
from .forms import LiberarTurmaForm, CriarReservaForm, PainelForm, FotoAvisoForm
from .models import Atividade, SistemaOperacional, TurmaAtividade, TipoAtividade, Software, Reserva, FotoAviso
from academico.models import Espaco
from contas.models import SuporteConta, Solicitante, TipoSolicitante

class IndexPublicoView(TemplateView):
	template_name = 'publico/painel.html'
	form_class = PainelForm

	def get(self, request, *args, **kwargs):		
		form = self.form_class()
		
		context = {
			'form': form
			}
		return render(request, self.template_name, context)

	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		reserva_list = None
		if form.is_valid():
			inicio = form.cleaned_data.get('inicio')
			fim = form.cleaned_data.get('fim')
			espaco = form.cleaned_data.get('espaco')
			reserva_list = Reserva.objects.filter(dia__range=[inicio, fim], espaco=espaco)


			dias = []
			
			atual = inicio
			
			while atual <= fim:
				dia = {}
				dia['dia'] = atual
				dia['Manha'] = True
				dia['Tarde'] = True
				dia['Noite'] = True
				
				reservas = reserva_list.filter(dia=atual)
				if reservas.count() > 0:
					#PERCORRE RESERAS DO DIA ATUAL, ATRIBUI FALSE PARA O TURNO EM QUESTÃO
					for reserva in reservas:
						dia[reserva.turno] = False
				
				dias.append(dia)
				atual = date.fromordinal(atual.toordinal()+1)
		else:
			pass
		
		form = self.form_class()
		context = {
			'form': form,
			'espaco' :espaco,
			'inicio' : inicio,
			'fim' : fim,
			'dias' : dias
			}
		return render(request, self.template_name, context)
			


	def get_context_data(self, **kwargs):
		context = super(IndexPublicoView, self).get_context_data(**kwargs)
		
		# try: 
		# 	id = self.kwargs['pk']
		# 	reservas = Reserva.objects.filter(turma__id=id, ativo=True)
		# except:
		# 	reservas = Reserva.objects.filter(ativo=True)

		# context['reservas'] = reservas
		
		return context

class IndexReservasView(LoginRequiredMixin, TemplateView):
	template_name = 'reservas/index_reservas.html'

	def get_context_data(self, **kwargs):
		context = super(IndexReservasView, self).get_context_data(**kwargs)

		turma = None
		try: 
			id = self.kwargs['pk']
			turma = TurmaAtividade.objects.get(id=id)
			reservas = Reserva.objects.filter(turma__id=id, ativo=True)
		except:
			turmas = TurmaAtividade.objects.filter(atividade__solicitante__id=self.request.user.id)
			reservas = Reserva.objects.filter(turma__id__in=turmas, ativo=True)

		context['reservas'] = reservas
		context['turma'] = turma
		
		return context



class IndexAtividadesView(LoginRequiredMixin, TemplateView):
	template_name = 'atividades/index_atividades.html'


class GerenciaAtividadesView(LoginRequiredMixin, TemplateView):
	template_name = 'atividades/gerencia/gerencia_atividades.html'


################### INICIO CRUD ATIVIDADE ##########################################3
class AtividadeListView(LoginRequiredMixin, ListView):
	model = Atividade
	template_name = 'atividades/atividade_list.html'

class AtividadeCreateView(LoginRequiredMixin, CreateView):
    template_name = "atividades/forms/atividade_form.html"
    model = Atividade
    form_class = AtividadeForm
    success_url = reverse_lazy("contas:index")

    def form_valid(self, form):
    	atividade = form.save(commit=False)
    	solicitante_count = Solicitante.objects.filter(id =self.request.user.id).count()
    	if solicitante_count == 1:
            solicitante = Solicitante.objects.get(id =self.request.user.id)
            atividade.solicitante = solicitante
            atividade.save()
            messages.add_message(self.request, messages.SUCCESS, 'Atividade salva com Sucesso! Aguarde um Responsável liberar a mesma')
    	else:
    	    messages.add_message(self.request, messages.ERROR, 'Erro ao salvar Atividade')
    	return HttpResponseRedirect(self.success_url)


class AtividadeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "atividades/forms/atividade_form.html"
    model = Atividade
    form_class = AtividadeForm
    success_url = reverse_lazy("contas:index")

    def form_valid(self, form):
    	atividade = form.save(commit=False)
    	solicitante_count = Solicitante.objects.filter(id =self.request.user.id).count()
    	if solicitante_count == 1:
    		solicitante = Solicitante.objects.get(id =self.request.user.id)
    		if atividade.solicitante == solicitante:
		    	atividade.save()
		    	messages.add_message(self.request, messages.SUCCESS, 'Atividade Editada com Sucesso!')
	    	else:
		    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Atividade')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Atividade')
    	return HttpResponseRedirect(self.success_url)



class AtividadeDetailView(LoginRequiredMixin, DetailView):
	model = Atividade
	
	#### para escolher qual o template usar
	def render_to_response(self, context, **response_kwargs):
		template_solicitante = 'atividades/atividade_solicitante_detail.html'
		template_suporte = 'atividades/atividade_suporte_detail.html'
		
		atividade  = context['object']
		usuario = context['view'].request.user
		turma_list = TurmaAtividade.objects.filter(atividade=atividade)
		context['turma_list'] = turma_list

		if usuario.permissao_suporte():
			template = template_suporte
		else:
			if atividade.solicitante.id == usuario.id:	
				template = template_solicitante
			else:
				messages.add_message(self.request, messages.ERROR, 'Acesso negado! Atividade não lhe pertence')
				return render(self.request, 'uteis/not_fund.html',context)

		return self.response_class(
			request = self.request,
			template = template,
			context = context, **response_kwargs
		)

class AtividadeDeleteView(LoginRequiredMixin, DeleteView):
	model = Atividade
	template_name = 'atividades/atividade_delete.html'
	success_url = reverse_lazy('contas:index')

############################ FIM CRUD ATIVIDADE ############################################


############################ INICIO CRUD TURMA ##############################################
class TurmaListView(LoginRequiredMixin, ListView):
	model = TurmaAtividade
	template_name = 'turmas/turma_list.html'
	
	def get_queryset(self):
		id = self.kwargs['pk']
		return TurmaAtividade.objects.filter(atividade__id=id)

	def get_context_data(self, **kwargs):
		context = super(TurmaListView, self).get_context_data(**kwargs)
		id = self.kwargs['pk']
		atividade = Atividade.objects.get(id=id)

		context['pk'] = id
		context['atividade'] = atividade
		
		return context

class TurmaCreateView(LoginRequiredMixin, CreateView):
	template_name = "turmas/forms/turma_form.html"
	model = TurmaAtividade
	form_class = TurmaAtividadeForm
	success_url = reverse_lazy("contas:index")

	def get_context_data(self, **kwargs):
		context = super(TurmaCreateView, self).get_context_data(**kwargs)
		context['atividade'] = Atividade.objects.get(id = self.kwargs['pk'])
		return context

	def form_valid(self, form):
		atividade = Atividade.objects.get(id = self.kwargs['pk'])
		# if not TurmaAtividade().verifica_criar_turma(atividade):
		# 	messages.add_message(self.request, messages.ERROR, 'Não é possivel criar uma turma para essa atividade, Existe turma não encerrada!')
		# 	return HttpResponseRedirect(self.success_url)


		turma = form.save(commit=False)
		softwares = form.cleaned_data.get('softwares')
		if self.request.user.permissao_solicitante:
			solicitante = Solicitante.objects.get(id=self.request.user.id)
			turma.solicitante = solicitante
			turma.atividade = atividade
			turma.responsavel = None
			turma.status = turma.CRIADA
			turma.momento = None
			turma.save()
			turma.softwares.set(softwares)
			messages.add_message(self.request, messages.SUCCESS, 'Turma salva com Sucesso! Aguarde até a turma ser liberada')
		else:
	    		messages.add_message(self.request, messages.ERROR, 'Erro ao salvar Turma')
		return HttpResponseRedirect(self.success_url)


class TurmaDetailView(LoginRequiredMixin, DetailView):
	model = TurmaAtividade
	# para escolher qual o template usar
	def render_to_response(self, context, **response_kwargs):
		template_solicitante = 'turmas/turma_solicitante_detail.html'
		template_suporte = 'turmas/turma_suporte_detail.html'
		usuario = context['view'].request.user
		if usuario.permissao_suporte():
			template = template_suporte
		elif usuario.permissao_solicitante():
			if context['object'].atividade.solicitante.id == usuario.id:	
				template = template_solicitante
			else:
				messages.add_message(self.request, messages.ERROR, 'Acesso negado! Turma não lhe pertence')
				return render(self.request, 'uteis/not_fund.html',context)

		return self.response_class(
			request = self.request,
			template = template,
			context = context, **response_kwargs
		)
	
class TurmaDeleteView(LoginRequiredMixin, DeleteView):
	model = TurmaAtividade
	template_name = 'turmas/turma_delete.html'
	success_url = reverse_lazy('contas:index')

	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		usuario = request.user
		if self.object.atividade.solicitante.id == usuario.id:
			try:
				self.object.delete()
				messages.add_message(self.request, messages.SUCCESS, 'Turma Deletada com Sucesso!')
			except:
				messages.add_message(self.request, messages.ERROR, 'Erro ao Deletar o Turma')
		else:
			messages.add_message(self.request, messages.ERROR, 'Erro ao Deletar o Turma, não apagada')
		return HttpResponseRedirect(self.get_success_url())

class TurmaUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "turmas/forms/turma_form.html"
    model = TurmaAtividade
    form_class = TurmaAtividadeForm
    success_url = reverse_lazy("contas:index")
		
    def form_valid(self, form):
        turma = form.save(commit=False)
        softwares = form.cleaned_data.get('softwares')
        if self.request.user.permissao_solicitante:
            solicitante = Solicitante.objects.get(id=self.request.user.id)
            turma.solicitante = solicitante
            turma.responsavel = turma.responsavel   
            turma.momento = turma.momento
            if turma.status == turma.ATIVA:
            	turma.status = turma.BLOQUEADA
            else:
            	turma.status = turma.status

            turma.save()
            turma.softwares.set(softwares)
	
            messages.add_message(self.request, messages.SUCCESS, 'Turma Editada com Sucesso! A mesma aguarda liberação da alteração')
        else:
                messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Turma')
        return HttpResponseRedirect(self.success_url)

class TurmaDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE Reserva ATIVOS QUE PERTENCAM A turma
		turma = TurmaAtividade.objects.get(id=pk)
		resultado = turma.dependencia()
		if not resultado['dependencia_reserva']:
			turma.ativo = False
			turma.status = turma.ENCERRADA
			turma.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")
################################ FIM CRUD TURMA ##########################################################

class LiberarTurmaView(LoginRequiredMixin, View):
	form_class =  LiberarTurmaForm
	template_name = 'turmas/forms/liberar_turma_form.html'
	redirect_url = reverse_lazy("contas:index")
    
	
	def get(self, request, *args, **kwargs):
		try:
			pk = self.kwargs['pk']
			turma =  TurmaAtividade.objects.get(id=pk)
			form = self.form_class(instance=turma)
		except:
			form = self.form_class()
		context = {
			'form': form
			}
		return render(request, self.template_name, context)


	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST)
		if form.is_valid():
			pk = self.kwargs['pk']
			turma = TurmaAtividade.objects.get(id=pk)
			turma.momento = form.cleaned_data.get('momento')
			turma.qtd_encontro = form.cleaned_data.get('qtd_encontro')
			turma.responsavel = SuporteConta.objects.get(id=request.user.id)
			espacos_liberados = form.cleaned_data.get('espacos_liberados')
			turma.espacos_liberados.set(espacos_liberados)
			turma.status = turma.ATIVA
			# print(turma.ATIVA)
			turma.save()

			return HttpResponseRedirect(self.redirect_url)
		return render(request, self.template_name, {'form':form})


class CriarReservaView(LoginRequiredMixin, View):
	
	template_name = 'turmas/forms/reservas_form.html'
	redirect_url = reverse_lazy("contas:index")
    
	
	def get(self, request, *args, **kwargs):
		pk = self.kwargs['pk']
		turma = TurmaAtividade.objects.get(id=pk)
		try:
			id_esp = self.kwargs['id_esp']
			espaco_atual = Espaco.objects.get(id=id_esp)
		except:
			espaco_atual = turma.espacos_liberados.first() 

		dias = []
		hoje = date.today()
		atual = turma.momento.inicio
		reservas_turma = Reserva.objects.filter(ativo=True, turma=turma)
		reservas_espaco = Reserva.objects.filter(ativo=True, espaco=espaco_atual)
		while atual <= turma.momento.termino:
			dia = {}
			dia['dia'] = atual
			if atual < hoje:
				dia['Manha'] = False
				dia['Tarde'] = False
				dia['Noite'] = False
			else:
				dia['Manha'] = True
				dia['Tarde'] = True
				dia['Noite'] = True
			#VERIFICA RESERVAS NO DIA ATUAL, PARA RESERVAS DA TURMA ATUAL
			reservas = reservas_turma.filter(dia=atual)
			if reservas.count() > 0:
				#PERCORRE RESERAS DO DIA ATUAL, ATRIBUI FALSE PARA O TURNO EM QUESTÃO
				for reserva in reservas:
					dia[reserva.turno] = False
			
			#VERIFICA SE EXISTE RESERVA NO DIA ATUAL EM OUTRAS TURMAS NO ESPACO
			reservas_esp = reservas_espaco.filter(dia=atual)
			if reservas_esp.count() > 0:
				for reserva in reservas_esp:
					dia[reserva.turno] = False
			dias.append(dia)
			atual = date.fromordinal(atual.toordinal()+1)
		
		reservas_restantes = Reserva.objects.filter(turma=turma).count()
		reservas_restantes = turma.qtd_encontro - reservas_restantes
		# passar um dicionario dos dias dizendo se esta livre
		context = {
			'espaco_list': turma.espacos_liberados,
			'turma': turma,
			'espaco_atual': espaco_atual,	
			'dias' : dias,
			'max_reservas' : turma.qtd_encontro,
			'reservas_restantes' : reservas_restantes
			}
		return render(request, self.template_name, context)
		
	def post(self, request, *args, **kwargs):
		dias_list = request.POST.getlist('dias[]')
		turma_id = request.POST.get('turma_id')
		espaco_id = request.POST.get('espaco_id')
		turma = TurmaAtividade.objects.get(id=turma_id)
		espaco = Espaco.objects.get(id=espaco_id)
		no_reserva = "Não realizadas "
		erro = False
		realizadas = 0
		for dia in dias_list:
			reservas_restantes = Reserva.objects.filter(turma=turma).count()
			reservas_restantes = turma.qtd_encontro - reservas_restantes
			reserva = Reserva()
			novo = dia.split("-")
			dia_padrao =  datetime.strptime(novo[0], "%d/%m/%Y").date()			
			reserva.dia = dia_padrao
			reserva.turno = novo[1]
			reserva.turma = turma
			reserva.espaco = espaco
			#VERIFICA SE EXISTE UMA RESERVA COM MESMO DIA, TURMA E TURNO
			reserva_existente_count = Reserva.objects.filter(ativo=True, turma=turma,dia=dia_padrao,turno=novo[1]).count()
			if reserva_existente_count > 0 or reservas_restantes <= 0:
				no_reserva += ' - {}, {}, {}'.format(novo[0], novo[1], espaco)
				erro = True
				# print(no_reserva)
				continue
			try:
				reserva.save()
				realizadas += 1
			except:
				erro = True
				# print(no_reserva)
				no_reserva += ' - {}, {}, {}'.format(novo[0], novo[1], espaco)
		
		if erro:
			messages.add_message(self.request, messages.ERROR, no_reserva)
		
		if realizadas > 0:
			messages.add_message(self.request, messages.SUCCESS, '{} Reservas realizadas com Sucesso!'.format(realizadas))

			


		resultado = {}
		data = json.dumps(resultado)

		# return render(request,	 'reservas/index_reservas.html', context)
		return HttpResponse(json.dumps(resultado), content_type="application/json")


class CancelarReservaAjax(LoginRequiredMixin, View):
	def get(self, request, pk):
		reserva = Reserva.objects.get(id=pk) 
		user = request.user
		resultado = {}
		#VERIFICA PERMISSÃO DO USUARIO PARA ATIVAR A ATIVIDADE
		if reserva.turma.atividade.solicitante.id == user.id:
			turma = reserva.turma
			reserva.delete()
			resultado['removel'] = True
		else:
			resultado['removel'] = False
		
		data = json.dumps(resultado)
		

		return HttpResponse(data, content_type="application/json")


class RemoverReservaAjax(LoginRequiredMixin, View):
	def get(self, request, *args, **kwargs):
		pk = self.kwargs['pk']
		reserva = Reserva.objects.get(id=pk) 
		user = request.user
		resultado = {}
		#VERIFICA PERMISSÃO DO USUARIO PARA ATIVAR A ATIVIDADE
		if reserva.turma.atividade.solicitante.id == user.id:
			dia = reserva.dia
			reserva.delete()
			resultado['removel'] = True
			messages.add_message(self.request, messages.SUCCESS, 'Reserva do dia {} Cancelada com Sucesso!'.format(dia))
		else:
			resultado['removel'] = False
		
		data = json.dumps(resultado)
		

		return HttpResponse(data, content_type="application/json")

#VERIFICAR NECESSIDADE, APAGAR
class MudarResponsavelViewAjax(LoginRequiredMixin, View):
	def get(self, request, pk):
		# print(request)
		turma = TurmaAtividade.objects.get(id=pk) 
		user = request.user
		resultado = turma.autualiza_responsavel(user)
		# html = render_to_string('atividades/includes/index_suporte.html',request=request,)

		return HttpResponse(json.dumps(resultado), content_type="application/json")

#ATIVA A ATIVIDADE POR AJAX
class AtividadeLiberarAjax(LoginRequiredMixin, View):
	def get(self, request, pk):
		atividade = Atividade.objects.get(id=pk) 
		user = request.user
		resultado = {}
		#VERIFICA PERMISSÃO DO USUARIO PARA ATIVAR A ATIVIDADE
		if user.permissao_suporte():
			atividade.liberada = True
			atividade.save()
			resultado['liberou'] = True
		else:
			resultado['liberou'] = False

		return HttpResponse(json.dumps(resultado), content_type="application/json")

	


####################### INICIO CRUD SISTEMA OPERACIONAL ##########################################
class SistemaOperacionalCreateView(LoginRequiredMixin, CreateView):
    template_name = "atividades/forms/gerencia/so_form.html"
    model = SistemaOperacional
    form_class = SistemaOperacionalForm
    success_url = reverse_lazy("atividade:listar_sistema")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	so = form.save(commit=False)
    	if self.request.user.permissao_suporte():
    		so.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Sistema Operacional Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar O Sistema Operacional')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class SistemaOperacionalUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "atividades/forms/gerencia/so_form.html"
    model = SistemaOperacional
    form_class = SistemaOperacionalForm
    success_url = reverse_lazy("atividade:listar_sistema")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	so = form.save(commit=False)
    	if self.request.user.permissao_suporte():
            dependencia = so.dependencia()
            if dependencia['dependencia_software']:
                lista = ''
                for dep in dependencia['software_list']:
                    lista += ' Software: {}.'.format(dep['software'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias Ativas, {}'.format(lista))
            else:
                so.save()
                messages.add_message(self.request, messages.SUCCESS, 'Sistema Operacional Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar O Sistema Operacional')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)


class SistemaOperacionalListView(LoginRequiredMixin, ListView):
    model = SistemaOperacional
    template_name = "atividades/gerencia/so_list.html"


class SistemaOperacionalDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE SOFTWARES ATIVOS QUE PERTENCAM AO SO
		sistema = SistemaOperacional.objects.get(id=pk)
		resultado = sistema.dependencia()
		if not resultado['dependencia_software']:
			sistema.ativo = False
			sistema.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


####################### FIM CRUD SISTEMA OPERACIONAL ##########################################

####################### INICIO CRUD TIPO ATIVIDADE ##########################################
class TipoAtividadeCreateView(LoginRequiredMixin, CreateView):
    template_name = "atividades/forms/gerencia/tipo_atividade_form.html"
    model = TipoAtividade
    form_class = TipoAtividadeForm
    success_url = reverse_lazy("atividade:listar_tipo_atividade")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	tipo_atividade = form.save(commit=False)
    	if self.request.user.permissao_suporte():
    		tipo_atividade.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Tipo de Atividade Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Tipo de Atividade')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class TipoAtividadeUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "atividades/forms/gerencia/tipo_atividade_form.html"
    model = TipoAtividade
    form_class = TipoAtividadeForm
    success_url = reverse_lazy("atividade:listar_tipo_atividade")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	tipo_atividade = form.save(commit=False)
    	if self.request.user.permissao_suporte():
            dependencia = tipo_atividade.dependencia()
            if dependencia['dependencia_atividade']:
                lista = ''
                for dep in dependencia['atividade_list']:
                    lista += ' Atividade: {}.'.format(dep['atividade'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias Ativas, {}'.format(lista))
            else:
                tipo_atividade.save()
                messages.add_message(self.request, messages.SUCCESS, 'Tipo de Atividade Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Tipo de Atividade')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class TipoAtividadeListView(LoginRequiredMixin, ListView):
    model = TipoAtividade
    template_name = "atividades/gerencia/tipo_atividade_list.html"

class TipoAtidadeDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE Atidades ATIVOS QUE PERTENCAM A tipo atividade
		tipo_atividade = TipoAtividade.objects.get(id=pk)
		resultado = tipo_atividade.dependencia()
		if not resultado['dependencia_atividade']:
			tipo_atividade.ativo = False
			tipo_atividade.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


####################### FIM CRUD TIPO ATIVIDADE ##########################################

####################### INICIO CRUD TIPO ATIVIDADE ##########################################
class SoftwareCreateView(LoginRequiredMixin, CreateView):
    template_name = "atividades/forms/gerencia/software_form.html"
    model = Software
    form_class = SoftwareForm
    success_url = reverse_lazy("atividade:listar_software")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	software = form.save(commit=False)
    	if self.request.user.permissao_suporte():
    		software.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Software Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Software')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class SoftwareUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "atividades/forms/gerencia/software_form.html"
    model = Software
    form_class = SoftwareForm
    success_url = reverse_lazy("atividade:listar_software")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	software = form.save(commit=False)
    	if self.request.user.permissao_suporte():
            dependencia = software.dependencia()
            if dependencia['dependencia_turma']:
                lista = ''
                for dep in dependencia['turma_list']:
                    lista += ' Turma: {}.'.format(dep['turma'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias Ativas, {}'.format(lista))
            else:
                software.save()
                messages.add_message(self.request, messages.SUCCESS, 'Software Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar o  Software')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class SoftwareListView(LoginRequiredMixin, ListView):
    model = Software
    template_name = "atividades/gerencia/software_list.html"

class SoftwareDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE SOFTWARES ATIVOS QUE PERTENCAM AO SO
		software = Software.objects.get(id=pk)
		resultado = software.dependencia()
		if not resultado['dependencia_turma']:
			software.ativo = False
			software.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


####################### FIM CRUD TIPO ATIVIDADE ##########################################

######################## INICIO CRUD FOTO AVISO #########################################

class FotoAvisoView(LoginRequiredMixin, View):
	form_class = FotoAvisoForm
	template_name = 'atividades/gerencia/foto_aviso_list.html'

	def get(self, request, *args, **kwargs):
		form = self.form_class
		fotos = FotoAviso.objects.filter(ativo=True)
		context = {
			'form': form,
			'fotos': fotos
		}
		return render(request, self.template_name, context)
	
	def post(self, request, *args, **kwargs):
		form = self.form_class(request.POST, request.FILES)
		print(form)
		if form.is_valid():
			foto = form.cleaned_data.get('foto')
			
			try:
				suporte = SuporteConta.objects.get(id=request.user.id)
				aviso_foto = FotoAviso(foto=foto, responsavel=suporte)
				aviso_foto.save()
				messages.add_message(self.request, messages.SUCCESS, 'Foto inserida')
			except:
				messages.add_message(self.request, messages.ERROR, 'Erro ao inserir a foto')
			
		context = {
			'form': form,
			'fotos': FotoAviso.objects.filter(ativo=True)
		}
		return render(request, self.template_name, context)

class FotoAvisoDeleteView(LoginRequiredMixin, DeleteView):
	model = FotoAviso
	template_name = 'atividades/gerencia/foto_aviso_delete.html'
	success_url = reverse_lazy('atividade:foto_aviso')


	def delete(self, request, *args, **kwargs):
		usuario = request.user
		if usuario.permissao_suporte:
			#verificar as turmas se existe alguma usando este PREDIO
			try:
				self.object = self.get_object()
				self.object.delete()
				messages.add_message(self.request, messages.SUCCESS, 'Foto Deletado com Sucesso!')
			except:
				# print('entrou no except')
				messages.add_message(self.request, messages.ERROR, 'Erro ao Deletar o Foto')
		else:
			# print('nao é suporte')
			messages.add_message(self.request, messages.ERROR, 'Erro ao Deletar o Foto')
		context = {
			'form': FotoAvisoForm,
			'fotos': FotoAviso.objects.filter(ativo=True)
		}
		return HttpResponseRedirect(self.get_success_url())


class TurmasReservasView(LoginRequiredMixin, View):
	model = TurmaAtividade
	template_name = 'reservas/escolher_turma.html'
	
	def get(self, request):
		user = self.request.user
		try:
			atividades = Atividade.objects.filter(solicitante=user)
			turmas = TurmaAtividade.objects.filter(atividade__id__in=atividades, status=TurmaAtividade.ATIVA)
			print(turmas)
		except:
			turmas = None
		
		context = {
			'turmas' : turmas
		}
		return render(request, self.template_name, context)

	# def get_context_data(self, **kwargs):
	# 	context = super(TurmasReservasListView, self).get_context_data(**kwargs)
	# 	id = self.kwargs['pk']
	# 	atividade = Atividade.objects.get(id=id)

	# 	context['pk'] = id
	# 	context['atividade'] = atividade
		
	# 	return context