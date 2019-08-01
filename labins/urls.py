"""sistemaEstagio URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

from django.contrib.auth.views import LoginView, LogoutView
# from core.views import IndexView

from django.conf import settings
from django.conf.urls.static import static

from core.forms import LoginForm

from atividades.views import IndexPublicoView
from atividades.models import FotoAviso

urlpatterns = [
    path('labins/admin/', admin.site.urls),
    
    # path('', IndexView.as_view(), name='index'),
    path('labins/conta/', include("contas.urls")),
    path('labins/atividade/', include("atividades.urls")),
    path('labins/academico/', include("academico.urls")),

    path('labins/painel-publico', IndexPublicoView.as_view(), name='publico'),

    path('labins/entrar',LoginView.as_view(authentication_form=LoginForm, extra_context={'fotos':FotoAviso.objects.filter(ativo=True)}), name='login'),
    path('labins/sair',LogoutView.as_view(), name='logout')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

