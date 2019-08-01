from django.contrib import admin

from .models import Atividade, TipoAtividade, Reserva
# Register your models here.

admin.site.register(TipoAtividade)
admin.site.register(Atividade)
admin.site.register(Reserva)