from django.shortcuts import render

from django.views.generic import View, TemplateView, CreateView, ListView, DetailView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from .models import Momento, CursoSetor, Predio, Campus, FotoPredio, Espaco, FotoEspaco, Sala
from atividades.models import TurmaAtividade
from .forms import MomentoForm, CursoSetorForm, PredioForm, CampusForm, FotoPredioForm
from .forms import EspacoForm, FotoEspacoForm, SalaForm


import json


####################### INICIO CRUD MOMENTO #########################################
class MomentoCreateView(LoginRequiredMixin, CreateView):
    template_name = "academico/forms/gerencia/momento_form.html"
    model = Momento
    form_class = MomentoForm
    success_url = reverse_lazy("academico:listar_momento")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	momento = form.save(commit=False)
    	if self.request.user.permissao_suporte():
    		momento.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Momento Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Momento')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class MomentoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "academico/forms/gerencia/momento_form.html"
    model = Momento
    form_class = MomentoForm
    success_url = reverse_lazy("academico:listar_momento")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	momento = form.save(commit=False)
    	if self.request.user.permissao_suporte():
            dependencia = momento.dependencia()
            if dependencia['dependencia_turma']:
                lista = ''
                for dep in dependencia['turma_list']:
                    lista += ' Turma: {}.'.format(dep['turma'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias ativas: {}'.format(lista))
            else:
                momento.save()
                messages.add_message(self.request, messages.SUCCESS, 'Momento Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Momento')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class MomentoListView(LoginRequiredMixin, ListView):
    model = Momento
    template_name = "academico/gerencia/momento_list.html"


class MomentoDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):

		momento = Momento.objects.get(id=pk)
		resultado = momento.dependencia()
		if not resultado['dependencia_turma']:
			momento.ativo = False
			momento.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


class CampusDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE PREDIOS OU CURSOS/SETORES ATIVOS QUE PERTENCAM AO CAMPUS
		campus = Campus.objects.get(id=pk)
		resultado = campus.dependencia()
		if not resultado['dependencia_curso_setor'] and not resultado['dependencia_predio']:
			campus.ativo = False
			campus.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


class PredioDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE SALAS ATIVAS QUE PERTENCAM AO PREDIO
		predio = Predio.objects.get(id=pk)
		resultado = predio.dependencia()
		if not resultado['dependencia_sala']:
			predio.ativo = False
			predio.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


class SalaDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE ESPACOS ATIVOS QUE PERTENCAM A SALA
		sala = Sala.objects.get(id=pk)
		resultado = sala.dependencia()
		if not resultado['dependencia_espaco']:
			sala.ativo = False
			sala.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


class EspacoDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE ESPACOS ATIVOS QUE PERTENCAM A SALA
		espaco = Espaco.objects.get(id=pk)
		espaco.ativo = False
		espaco.save()
		resultado = {
			'desativou' : True
		}
		return HttpResponse(json.dumps(resultado), content_type="application/json")

####################### FIM CRUD MOMENTO ###########################################

####################### INICIO CRUD CURSO SETOR #####################################
class CursoSetorCreateView(LoginRequiredMixin, CreateView):
    template_name = "academico/forms/gerencia/curso_setor_form.html"
    model = CursoSetor
    form_class = CursoSetorForm
    success_url = reverse_lazy("academico:listar_curso_setor")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	curos_setor = form.save(commit=False)
    	if self.request.user.permissao_suporte():
    		curos_setor.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Curso/Setor Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Curso/Setor')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class CursoSetorUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "academico/forms/gerencia/curso_setor_form.html"
    model = CursoSetor
    form_class = CursoSetorForm
    success_url = reverse_lazy("academico:listar_curso_setor")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	curso_setor = form.save(commit=False)
    	if self.request.user.permissao_suporte():
            dependencia = curso_setor.dependencia()
            lista = ''
            if dependencia['dependencia_solicitante'] or dependencia['dependencia_atividade']:
                for dep in dependencia['solicitante_list']:
                    lista += ' Solicitante: {}.'.format(dep['solicitante'])

                for dep in dependencia['atividade_list']:
                    lista += ' Atividade/Disciplina: {}.'.format(dep['atividade'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias ativas: {}'.format(lista))
            else:
                curso_setor.save()
                messages.add_message(self.request, messages.SUCCESS, 'Curso/Setor Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Curso/Setor')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class CursoSetorListView(LoginRequiredMixin, ListView):
    model = CursoSetor
    template_name = "academico/gerencia/curso_setor_list.html"


class CursoSetorDesativarAjaxView(LoginRequiredMixin, View):
	def get(self, request, pk):
		# #VERIFICAR SE EXISTE ESPACOS ATIVOS QUE PERTENCAM A SALA
		curso_setor = CursoSetor.objects.get(id=pk)
		resultado = curso_setor.dependencia()
		if not resultado['dependencia_solicitante'] and not resultado['dependencia_atividade']:
			curso_setor.ativo = False
			curso_setor.save()
		return HttpResponse(json.dumps(resultado), content_type="application/json")


####################### FIM CRUD CURSO SETOR ########################################

####################### INICIO CRUD PREDIO ##########################################
class PredioCreateView(LoginRequiredMixin, CreateView):
    template_name = "academico/forms/gerencia/predio_form.html"
    model = Predio
    form_class = PredioForm
    success_url = reverse_lazy("academico:listar_predio")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	predio = form.save(commit=False)
    	if self.request.user.permissao_suporte():
    		predio.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Prédio Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Prédio')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class PredioUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "academico/forms/gerencia/predio_form.html"
    model = Predio
    form_class = PredioForm
    success_url = reverse_lazy("academico:listar_predio")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	predio = form.save(commit=False)
    	if self.request.user.permissao_suporte():
            dependencia = predio.dependencia()
            if dependencia['dependencia_sala']:
                lista = ''
                for dep in dependencia['sala_list']:
                    lista += ' Sala: {}.'.format(dep['sala'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias ativas: {}'.format(lista))
            else:
                predio.save()
                messages.add_message(self.request, messages.SUCCESS, 'Prédio Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Prédio')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class PredioListView(LoginRequiredMixin, ListView):
    model = Predio
    template_name = "academico/gerencia/predio_list.html"


####################### FIM CRUD PREDIO ###############################################



class PredioDetailView(LoginRequiredMixin, DetailView):
	template_name = "academico/gerencia/fotos_predio_espaco.html"
	model = Predio

	def get(self, request, **kwargs):
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		context['fotos'] = FotoPredio.objects.filter(predio__id=self.object.id)
		form = FotoPredioForm()
		context['form'] = form
		return self.render_to_response(context)
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = FotoPredioForm(request.POST, request.FILES)
		if form.is_valid():
			foto = FotoPredio(predio=self.object, foto=form.cleaned_data['foto'])
			foto.save()
			messages.add_message(self.request, messages.SUCCESS, 'Foto adicionada com sucesso!')
		else:
			messages.add_message(self.request, messages.ERROR, 'Algo de Errado não esta Certo!')
			
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		context['fotos'] = FotoPredio.objects.filter(predio__id=self.object.id)
		form = FotoPredioForm()
		context['form'] = form
		return self.render_to_response(context)



class FotoPredioDeleteView(LoginRequiredMixin, DeleteView):
	model = FotoPredio
	template_name = 'academico/gerencia/foto_predio_espaco_delete.html'
	success_url = reverse_lazy('academico:listar_predio')


	def delete(self, request, *args, **kwargs):
		usuario = request.user
		if usuario.permissao_suporte:
			#verificar as turmas se existe alguma usando este PREDIO
			try:
				self.object = self.get_object()
				predio = self.object.predio
				print(predio)
				context = {
				'object' : predio
				}
				self.object.delete()
				messages.add_message(self.request, messages.SUCCESS, 'Foto Deletado com Sucesso!')
				return HttpResponse(request,'academico/gerencia/fotos_predio_espaco.html', context)
			except:
				# print('entrou no except')
				messages.add_message(self.request, messages.ERROR, 'Erro ao Deletar o Foto')
		else:
			# print('nao é suporte')
			messages.add_message(self.request, messages.ERROR, 'Erro ao Deletar o Foto')
		return HttpResponseRedirect(self.get_success_url())

####################### FIM FOTO PREDIO #############################################

####################### INICIO CRUD SALA ##########################################
class SalaCreateView(LoginRequiredMixin, CreateView):
    template_name = "academico/forms/gerencia/sala_form.html"
    model = Sala
    form_class = SalaForm
    success_url = reverse_lazy("academico:listar_sala")
    index_url = reverse_lazy("index")

    def form_valid(self, form):
    	sala = form.save(commit=False)
    	if self.request.user.permissao_suporte:
    		sala.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Sala Salva com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Sala')
	    	return HttpResponseRedirect(self.index_url)
    	return HttpResponseRedirect(self.success_url)
	
class SalaListView(LoginRequiredMixin, ListView):
    model = Sala
    template_name = "academico/gerencia/sala_list.html"

class SalaUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "academico/forms/gerencia/sala_form.html"
    model = Sala
    form_class = SalaForm
    success_url = reverse_lazy("academico:listar_sala")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	sala = form.save(commit=False)
    	if self.request.user.permissao_suporte:
            dependencia = sala.dependencia()
            if dependencia['dependencia_espaco']:
                lista = ''
                for dep in dependencia['espaco_list']:
                    lista += ' Espaço: {}.'.format(dep['espaco'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias Ativas, {}'.format(lista))
            else:
                sala.save()
                messages.add_message(self.request, messages.SUCCESS, 'Sala Editada com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Sala')
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)


####################### INICIO CRUD ESPAÇO ##########################################
class EspacoCreateView(LoginRequiredMixin, CreateView):
    template_name = "academico/forms/gerencia/espaco_form.html"
    model = Espaco
    form_class = EspacoForm
    success_url = reverse_lazy("academico:listar_espaco")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	espaco = form.save(commit=False)
    	if self.request.user.permissao_suporte:
    		espaco.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Espaço Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Espaço')
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class EspacoListView(LoginRequiredMixin, ListView):
    model = Espaco
    template_name = "academico/gerencia/espaco_list.html"

class EspacoUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "academico/forms/gerencia/espaco_form.html"
    model = Espaco
    form_class = EspacoForm
    success_url = reverse_lazy("academico:listar_espaco")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	espaco = form.save(commit=False)
    	if self.request.user.permissao_suporte:
    		espaco.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Espaço Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Espaço')
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

####################### FIM DO CRUDO ESPACO #############################################

####################### INICIO FOTO ESPACO ############################################
class FotoEspacoCreateView(LoginRequiredMixin, CreateView):
	template_name = "academico/forms/gerencia/foto_local_form.html"
	model = FotoEspaco
	form_class = FotoEspacoForm
	success_url = reverse_lazy("academico:listar_espaco")
	login_url = reverse_lazy("login")
	
	def get_context_data(self, **kwargs):
		context = super(FotoEspacoCreateView, self).get_context_data(**kwargs)
		pk = self.kwargs['pk']
		context['id'] = pk
		context['espaco'] = True
		return context 

	def form_valid(self, form):
		foto = form.save(commit=False)
		if self.request.user.permissao_suporte:
			#pega o id do espaço passado por get pelo url
			pk = self.kwargs['pk']
			espaco = Espaco.objects.get(id=pk)
			foto.espaco = espaco
			foto.save()
			messages.add_message(self.request, messages.SUCCESS, 'Foto do Espaço Salvo com Sucesso!')
		else:
			messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Foto do Espaço')
			return HttpResponseRedirect(self.login_url)
		return HttpResponseRedirect(self.success_url)

class EspacoDetailView(LoginRequiredMixin, DetailView):
	template_name = "academico/gerencia/fotos_predio_espaco.html"
	model = Espaco

	def get(self, request, **kwargs):
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		context['fotos'] = FotoEspaco.objects.filter(espaco__id=self.object.id)
		form = FotoEspacoForm()
		context['form'] = form
		return self.render_to_response(context)
		
	def post(self, request, *args, **kwargs):
		self.object = self.get_object()
		form = FotoEspacoForm(request.POST, request.FILES)
		if form.is_valid():
			foto = FotoEspaco(espaco=self.object, foto=form.cleaned_data['foto'])
			foto.save()
			messages.add_message(self.request, messages.SUCCESS, 'Foto adicionada com sucesso!')
		else:
			messages.add_message(self.request, messages.ERROR, 'Algo de Errado não esta Certo!')
			
		self.object = self.get_object()
		context = self.get_context_data(object=self.object)
		context['fotos'] = FotoEspaco.objects.filter(espaco__id=self.object.id)
		form = FotoEspacoForm()
		context['form'] = form
		return self.render_to_response(context)

class FotoEspacoDeleteView(LoginRequiredMixin, DeleteView):
	model = FotoEspaco
	template_name = 'academico/gerencia/foto_predio_espaco_delete.html'
	success_url = reverse_lazy('academico:listar_espaco')

	def delete(self, request, *args, **kwargs):
		usuario = request.user
		if usuario.permissao_suporte:
			#verificar as turmas se existe alguma usando esta foto
			try:
				self.object = self.get_object()
				self.object.delete()
				messages.add_message(self.request, messages.SUCCESS, 'Foto do Espaço Deletado com Sucesso!')
			except:
				# print('entrou no except')
				messages.add_message(self.request, messages.ERROR, 'Erro ao Deletar o Foto do Espaço')
		else:
			# print('nao é suporte')
			messages.add_message(self.request, messages.ERROR, 'Erro ao Deletar o Foto do Espaço')
		return HttpResponseRedirect(self.get_success_url())

####################### FIM FOTO ESPACO #############################################

####################### INICIO CAMPUS ##############################################
class CampusCreateView(LoginRequiredMixin, CreateView):
    template_name = "academico/forms/gerencia/campus_form.html"
    model = Campus
    form_class = CampusForm
    success_url = reverse_lazy("academico:listar_campus")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	campus = form.save(commit=False)
    	if self.request.user.permissao_suporte:
    		campus.save()
    		messages.add_message(self.request, messages.SUCCESS, 'Campus Salvo com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Salvar Campus')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class CampusUpdateView(LoginRequiredMixin, UpdateView):
    template_name = "academico/forms/gerencia/campus_form.html"
    model = Campus
    form_class = CampusForm
    success_url = reverse_lazy("academico:listar_campus")
    login_url = reverse_lazy("login")

    def form_valid(self, form):
    	campus = form.save(commit=False)
    	if self.request.user.permissao_suporte:
            dependencia = campus.dependencia()
            lista = ''
            if dependencia['dependencia_predio'] or dependencia['dependencia_curso_setor']:
                for dep in dependencia['predio_list']:
                    lista += ' Predio: {}.'.format(dep['predio'])
            
                for dep in dependencia['curso_setor_list']:
                    lista += ' Curso/Setor: {}.'.format(dep['curso_setor'])
                messages.add_message(self.request, messages.ERROR, 'Não Editado, Existem Dependencias ativas: {}'.format(lista))
            else:
                campus.save()
                messages.add_message(self.request, messages.SUCCESS, 'Campus Editado com Sucesso!')
    	else:
	    	messages.add_message(self.request, messages.ERROR, 'Erro ao Editar Campus')
	    	# login_url = reverse_lazy("login")
	    	return HttpResponseRedirect(self.login_url)
    	return HttpResponseRedirect(self.success_url)

class CampusListView(LoginRequiredMixin, ListView):
    model = Campus
    template_name = "academico/gerencia/campus_list.html"


####################### FIM CAMPUS ##########################################
