from django.urls import path

from .views import MomentoCreateView, MomentoListView, MomentoUpdateView 
from .views import CursoSetorCreateView, CursoSetorListView, CursoSetorUpdateView, CursoSetorDesativarAjaxView
from .views import PredioCreateView, PredioListView, PredioUpdateView, PredioDesativarAjaxView
from .views import CampusCreateView, CampusListView, CampusUpdateView
from .views import PredioDetailView, FotoPredioDeleteView
from .views import EspacoCreateView, EspacoListView, EspacoUpdateView, EspacoDesativarAjaxView
from .views import FotoEspacoCreateView, EspacoDetailView, FotoEspacoDeleteView
from .views import SalaCreateView, SalaListView, SalaUpdateView, SalaDesativarAjaxView
from .views import MomentoDesativarAjaxView
from .views import CampusDesativarAjaxView


app_name = "academico"
urlpatterns = [
    path('momento/novo', MomentoCreateView.as_view(), name='novo_momento'),
    path('momento/listar', MomentoListView.as_view(), name='listar_momento'),
    path('momento/editar/<uuid:pk>', MomentoUpdateView.as_view(), name='editar_momento'),    
    
    path('momento/desativar-ajax/<uuid:pk>', MomentoDesativarAjaxView.as_view(), name='desativar_momento_ajax'),

    path('curso-setor/novo', CursoSetorCreateView.as_view(), name='novo_curso_setor'),
    path('curso-setor/listar', CursoSetorListView.as_view(), name='listar_curso_setor'),
    path('curso-setor/editar/<uuid:pk>', CursoSetorUpdateView.as_view(), name='editar_curso_setor'),
    path('curso-setor/desativar-ajax/<uuid:pk>', CursoSetorDesativarAjaxView.as_view(), name='desativar_curso_setor_ajax'),

    path('predio/novo', PredioCreateView.as_view(), name='novo_predio'),
    path('predio/listar', PredioListView.as_view(), name='listar_predio'),
    path('predio/editar/<uuid:pk>', PredioUpdateView.as_view(), name='editar_predio'),
    path('predio/desativar-ajax/<uuid:pk>', PredioDesativarAjaxView.as_view(), name='desativar_predio_ajax'),
    

    path('fotos-predio/<uuid:pk>', PredioDetailView.as_view(), name='fotos_predio'),
    # path('foto-predio/nova/<uuid:pk>', FotoPredioCreateView.as_view(), name='novo_foto_predio'),
    path('foto-predio/delete/<uuid:pk>', FotoPredioDeleteView.as_view(), name='deletar_foto_predio'),
    
    path('sala/novo', SalaCreateView.as_view(), name='novo_sala'),
    path('sala/listar', SalaListView.as_view(), name='listar_sala'),
    path('sala/editar/<uuid:pk>', SalaUpdateView.as_view(), name='editar_sala'),
    path('sala/desativar-ajax/<uuid:pk>', SalaDesativarAjaxView.as_view(), name='desativar_sala_ajax'),


    path('espaco/novo', EspacoCreateView.as_view(), name='novo_espaco'),
    path('espaco/listar', EspacoListView.as_view(), name='listar_espaco'),
    path('espaco/editar/<uuid:pk>', EspacoUpdateView.as_view(), name='editar_espaco'),
    path('espaco/destivar-ajax/<uuid:pk>', EspacoDesativarAjaxView.as_view(), name='desativar_espaco_ajax'),

    path('fotos-espaco/<uuid:pk>', EspacoDetailView.as_view(), name='fotos_espaco'),
    path('foto-espaco/nova/<uuid:pk>', FotoEspacoCreateView.as_view(), name='novo_foto_espaco'),
    path('foto-espaco/deletar/<uuid:pk>', FotoEspacoDeleteView.as_view(), name='deletar_foto_espaco'),

    path('campus/novo', CampusCreateView.as_view(), name='novo_campus'),
    path('campus/listar', CampusListView.as_view(), name='listar_campus'),
    path('campus/editar/<uuid:pk>', CampusUpdateView.as_view(), name='editar_campus'),
    path('campus/desativar-ajax/<uuid:pk>', CampusDesativarAjaxView.as_view(), name='desativar_campus_ajax'),

]