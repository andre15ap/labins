from django.urls import path

from .views import IndexReservasView, IndexAtividadesView, GerenciaAtividadesView
#VERIFICAR SE AINDA VAI NECESSITAR DE MUDAR RESPONSAVEL
from .views import MudarResponsavelViewAjax

from .views import AtividadeLiberarAjax, RemoverReservaAjax

from .views import AtividadeCreateView, AtividadeListView, AtividadeDeleteView,AtividadeUpdateView, AtividadeDetailView
from .views import TipoAtividadeCreateView, TipoAtividadeListView, TipoAtividadeUpdateView
from .views import SistemaOperacionalCreateView, SistemaOperacionalUpdateView, SistemaOperacionalListView, SistemaOperacionalDesativarAjaxView
from .views import SoftwareCreateView, SoftwareListView, SoftwareUpdateView, SoftwareDesativarAjaxView
from .views import TurmaListView, TurmaCreateView, TurmaUpdateView, TurmaDetailView, TurmaDesativarAjaxView
from .views import LiberarTurmaView, CriarReservaView
from .views import TipoAtidadeDesativarAjaxView
from .views import FotoAvisoView, FotoAvisoDeleteView
from .views import TurmasReservasView

app_name = "atividade"
urlpatterns = [
    path('', IndexAtividadesView.as_view(), name='index_atividade'),
    path('reservas/<uuid:pk>', IndexReservasView.as_view(), name='index_reservas'),
    path('reservas', IndexReservasView.as_view(), name='index_reservas'),
    
    path('gerencia', GerenciaAtividadesView.as_view(), name='gerencia'),
    
    path('nova', AtividadeCreateView.as_view(), name='nova_atividade'),
    path('listar', AtividadeListView.as_view(), name='listar_atividade'),
    path('detalhar/<uuid:pk>', AtividadeDetailView.as_view(), name='atividade_detail'),
    path('delete/<uuid:pk>', AtividadeDeleteView.as_view(), name='atividade_delete'),
    path('update/<uuid:pk>', AtividadeUpdateView.as_view(), name='atividade_update'),
    
    path('turma/nova/<uuid:pk>', TurmaCreateView.as_view(), name='nova_turma'),
    path('turma/listar/<uuid:pk>', TurmaListView.as_view(), name='listar_turma'),
    path('turma/escolher', TurmasReservasView.as_view(), name='escolher_turma'),
    path('turma/editar/<uuid:pk>', TurmaUpdateView.as_view(), name='editar_turma'),
    path('turma/detalhar/<uuid:pk>', TurmaDetailView.as_view(), name='detalhar_turma'),
    path('turma/desativar-ajax/<uuid:pk>', TurmaDesativarAjaxView.as_view(), name='desativar_turma_ajax'),
    
    
    path('turma/liberar/<uuid:pk>', LiberarTurmaView.as_view(), name='liberar_turma'),
    
    path('reserva/nova/<uuid:pk>', CriarReservaView.as_view(), name='nova_reserva'),
    path('reserva/nova/<uuid:pk>/<uuid:id_esp>', CriarReservaView.as_view(), name='nova_reserva'),
    path('reserva/nova', CriarReservaView.as_view(), name='nova_reserva'),


    path('so/novo', SistemaOperacionalCreateView.as_view(), name='novo_sistema'),
    path('so/listar', SistemaOperacionalListView.as_view(), name='listar_sistema'),
    path('so/editar/<uuid:pk>', SistemaOperacionalUpdateView.as_view(), name='editar_sistema'),
    path('so/desativar-ajax/<uuid:pk>', SistemaOperacionalDesativarAjaxView.as_view(), name='desativar_sistema_ajax'),
    
    path('tipo-atividade/novo', TipoAtividadeCreateView.as_view(), name='novo_tipo_atividade'),
    path('tipo-atividade/listar', TipoAtividadeListView.as_view(), name='listar_tipo_atividade'),
    path('tipo-atividade/editar/<uuid:pk>', TipoAtividadeUpdateView.as_view(), name='editar_tipo_atividade'),
    path('tipo-atividade/desativar-ajax/<uuid:pk>', TipoAtidadeDesativarAjaxView.as_view(), name='desativar_tipo_atividade_ajax'),
    
    path('software/novo', SoftwareCreateView.as_view(), name='novo_software'),
    path('software/listar', SoftwareListView.as_view(), name='listar_software'),
    path('software/editar/<uuid:pk>', SoftwareUpdateView.as_view(), name='editar_software'),
    path('software/desativar-ajax/<uuid:pk>', SoftwareDesativarAjaxView.as_view(), name='desativar_software_ajax'),

    path('atividade-ativar/<uuid:pk>', AtividadeLiberarAjax.as_view(), name='atividade_liberar_ajax'),
    
    path('remover-reserva/<uuid:pk>', RemoverReservaAjax.as_view(), name='reserva_remover_ajax'),

    path('turma-mudar-responsavel/<uuid:pk>', MudarResponsavelViewAjax.as_view(), name='mudar_responsavel_ajax'),
    
    path('fotos-avisos', FotoAvisoView.as_view(), name='foto_aviso'),
    path('foto-aviso-delete/<uuid:pk>', FotoAvisoDeleteView.as_view(), name='foto_aviso_delete'),

]