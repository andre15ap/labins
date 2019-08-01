
from django.urls import path

from .views import IndexListView, SolicitanteCreateView, HomeView,SolicitanteListView, SolicitanteDetailView
from .views import SolicitanteLiberaAjax, SolicitanteDesativarAjaxView
from .views import LstarTurmasAjax
from .views import TipoSolicitanteCreateView, TipoSolicitanteListView, TipoSolicitanteUpdateView, TipoSolicitanteDesativarAjaxView
from .views import UsuarioView, SuporteAtualizarDadosView, SolicitanteAtualizarDadosView, AlterarSenhaView
from .views import SuporteDetailView, RecupararSenhaView

app_name = "contas"
urlpatterns = [
    path('', IndexListView.as_view(), name='index'),
    path('registrar/', SolicitanteCreateView.as_view(), name='registrar'),
    path('recuperar-senha/', RecupararSenhaView.as_view(), name='recuperar_senha'),
    
    path('usuario/', UsuarioView.as_view(), name='usuario_detail'),
    path('solicitante/atualizar/<uuid:pk>', SolicitanteAtualizarDadosView.as_view(), name='solicitante_update'),
    path('suporte/atualizar/<uuid:pk>', SuporteAtualizarDadosView.as_view(), name='suporte_update'),
    path('usuario/alterar-senha', AlterarSenhaView.as_view(), name='usuario_alterar_senha'),
    
    
    path('suporte/detalhar/<uuid:pk>', SuporteDetailView.as_view(), name='suporte_detail'),

    path('solicitantes/', SolicitanteListView.as_view(), name='solicitantes_list'),
    path('solicitante/<uuid:pk>', SolicitanteDetailView.as_view(), name='solicitante_detail'),
    path('solicitante/desativar-ajax/<uuid:pk>', SolicitanteDesativarAjaxView.as_view(), name='desativar_solicitante_ajax'),

    path('solicitante/libera-ajax/<uuid:pk>', SolicitanteLiberaAjax.as_view(), name='solicitante_liberar_ajax'),
    path('turma/listar/<uuid:pk>', LstarTurmasAjax.as_view(), name='listar_turmas_ajax'),
    
    path('tipo-solicitante/novo', TipoSolicitanteCreateView.as_view(), name='novo_tipo_solicitante'),
    path('tipo-solicitante/listar', TipoSolicitanteListView.as_view(), name='listar_tipo_solicitante'),
    path('tipo-solicitante/editar/<uuid:pk>', TipoSolicitanteUpdateView.as_view(), name='editar_tipo_solicitante'),
    path('tipo-solicitante/desativar-ajax/<uuid:pk>', TipoSolicitanteDesativarAjaxView.as_view(), name='desativar_tipo_solicitante_ajax'),
    

    path('home', HomeView.as_view(), name='home')
]