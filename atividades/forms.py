from django import forms

from .models import Atividade, SistemaOperacional, TipoAtividade, Software, TurmaAtividade, Reserva, FotoAviso
from academico.models import Momento, Espaco, CursoSetor

class AtividadeForm(forms.ModelForm):
    class Meta:
        model = Atividade
        fields = ('nome', 'descricao','tipo_atividade', 'curso_setor') 

        labels = ({
            'tipo_atividade' : 'Tipo da atividade', 
            'curso_setor' : 'Curso ou Setor'
        })


    def __init__(self, *args, **kwargs):
        super(AtividadeForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs = {'class': 'form-control','placeholder':'Nome da atividade'}
        self.fields['descricao'].widget.attrs = {'class': 'form-control','rows': 3, 'cols': 40, 'style':'resize:none','placeholder':'Descrição da atividade'}
        self.fields['tipo_atividade'].widget.attrs = {'class': 'form-control'}
        self.fields['curso_setor'].widget.attrs = {'class': 'form-control'}
        self.fields['curso_setor'].queryset = CursoSetor.objects.filter(ativo=True)
        # for field in iter(self.fields):
        #     self.fields[field].widget.attrs.update({
        #         'class': 'form-control'
        # })


class SistemaOperacionalForm(forms.ModelForm):
    class Meta:
        model = SistemaOperacional
        fields = ('nome', 'versao') 

    def __init__(self, *args, **kwargs):
        super(SistemaOperacionalForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control',
                'placeholder': '{} do sistema'.format(field)
        })


class TipoAtividadeForm(forms.ModelForm):
    class Meta:
        model = TipoAtividade
        fields = ('identificador', 'descricao') 

    def __init__(self, *args, **kwargs):
        super(TipoAtividadeForm, self).__init__(*args, **kwargs)
        self.fields['identificador'].widget.attrs = {'class': 'form-control','placeholder':'Identificador do tipo de atividade'}
        self.fields['descricao'].widget.attrs = {'class': 'form-control','rows': 3, 'cols': 40, 'style':'resize:none','placeholder':'Descrição do tipo de atividade'}


class SoftwareForm(forms.ModelForm):
    class Meta:
        model = Software
        fields = ('nome', 'sistema', 'descricao') 

    def __init__(self, *args, **kwargs):
        super(SoftwareForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs = {'class': 'form-control','placeholder':'Nome do Software'}
        self.fields['sistema'].widget.attrs = {'class': 'form-control'}
        self.fields['descricao'].widget.attrs = {'class': 'form-control','rows': 3, 'cols': 40, 'style':'resize:none','placeholder':'Descrição do Software'}
        self.fields['sistema'].queryset = SistemaOperacional.objects.filter(ativo=True)

class TurmaAtividadeForm(forms.ModelForm):    
    class Meta:
        model = TurmaAtividade
        fields = ('nome', 'softwares', 'qtd_computadores','qtd_bancadas') 

    def __init__(self, *args, **kwargs):
        super(TurmaAtividadeForm, self).__init__(*args, **kwargs)
        # print('---- form {}'.format(kwargs))
        self.fields['nome'].widget.attrs = {'class':'form-control', 'placeholder': 'Nome da turma'}
        self.fields['softwares'].widget.attrs = {'class':'form-control'}
        self.fields['qtd_computadores'].widget.attrs = {'class':'form-control','placeholder':'Quantidade de computadores'}
        self.fields['qtd_bancadas'].widget.attrs = {'class':'form-control','placeholder':'Quantidade de bancadas'}
        self.fields['softwares'].queryset = Software.objects.filter(ativo=True)

class LiberarTurmaForm(forms.ModelForm):

    class Meta:
        model = TurmaAtividade
        fields = ('momento','qtd_encontro', 'espacos_liberados')
    
    def __init__(self, *args, **kwargs):
        super(LiberarTurmaForm, self).__init__(*args, **kwargs)
        self.fields['momento'].widget.attrs = {'class':'form-control', 'required':True}
        self.fields['qtd_encontro'].widget.attrs = {'class':'form-control', 'required':False}
        self.fields['espacos_liberados'].widget.attrs = {'class':'form-control', 'required':True}
        self.fields['momento'].queryset = Momento.objects.filter(ativo=True)
        self.fields['espacos_liberados'].queryset = Espaco.objects.filter(ativo=True)

class CriarReservaForm(forms.ModelForm):
    # espaco = forms.ModelChoiceField(queryset=Espaco.objects.filter(ativo=True))
    class Meta:
        model = Reserva
        fields = ('dia', 'turno','espaco')
    
    def __init__(self, *args, **kwargs):
        super(CriarReservaForm, self).__init__(*args, **kwargs)
        self.fields['dia'].widget.attrs = {'class': 'form-control calendario', 'required':True}
        self.fields['turno'].widget.attrs = {'class': 'form-control', 'required':True}
        self.fields['espaco'].widget.attrs = {'class': 'form-control', 'required':True}
        

import datetime  
class PainelForm(forms.Form):
    # inicio = forms.DateField(initial=datetime.date.today)
    inicio = forms.DateField()
    fim = forms.DateField()
    espaco = forms.ModelChoiceField(queryset=Espaco.objects.filter(ativo=True))


    def __init__(self, *args, **kwargs):
        super(PainelForm, self).__init__(*args, **kwargs)
        self.fields['inicio'].widget.attrs = {'class': 'form-control calendario','placeholder':'Data Início', 'required':True}
        self.fields['fim'].widget.attrs = {'class': 'form-control calendario', 'placeholder': 'Data Fim', 'required':True}
        self.fields['espaco'].widget.attrs = {'class': 'form-control', 'placeholder': 'Espaço', 'title':'Selecione o Espaço', 'required':True}
        

class FotoAvisoForm(forms.ModelForm):
    class Meta:
        model = FotoAviso
        fields = ('foto',) 

    def __init__(self, *args, **kwargs):
        super(FotoAvisoForm, self).__init__(*args, **kwargs)
        self.fields['foto'].widget.attrs = {'class': 'form-control-file'}