from django import forms

from .models import Momento, CursoSetor, Predio, Campus, FotoPredio, Espaco, FotoEspaco, Sala


class MomentoForm(forms.ModelForm):
    class Meta:
        model = Momento
        fields = ('identificador', 'inicio', 'termino', 'ativo') 

    def __init__(self, *args, **kwargs):
        super(MomentoForm, self).__init__(*args, **kwargs)
        self.fields['identificador'].widget.attrs = {'class': 'form-control','placeholder':'Nome do Momento'}
        self.fields['inicio'].widget.attrs = {'class': 'form-control calendario'}
        self.fields['termino'].widget.attrs = {'class': 'form-control calendario'}
        # self.fields['ativo'].widget.attrs = {'class': 'form-control'}

class CursoSetorForm(forms.ModelForm):
    class Meta:
        model = CursoSetor
        fields = ('nome', 'campus', 'tipo') 

    def __init__(self, *args, **kwargs):
        super(CursoSetorForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs = {'class': 'form-control','placeholder':'Nome do curso/setor'}
        self.fields['campus'].widget.attrs = {'class': 'form-control','placeholder':'Campus do curso/setor'}
        self.fields['tipo'].widget.attrs = {'class': 'form-control'}
        self.fields['campus'].queryset = Campus.objects.filter(ativo=True)

class PredioForm(forms.ModelForm):
    class Meta:
        model = Predio
        fields = ('identificador', 'descricao', 'campus') 

    def __init__(self, *args, **kwargs):
        super(PredioForm, self).__init__(*args, **kwargs)
        self.fields['identificador'].widget.attrs = {'class': 'form-control','placeholder':'Identificador do Prédio'}
        self.fields['descricao'].widget.attrs = {'class': 'form-control','rows': 3, 'cols': 40, 'style':'resize:none','placeholder':'Informação extra'}
        self.fields['campus'].widget.attrs = {'class': 'form-control'}
        self.fields['campus'].queryset = Campus.objects.filter(ativo=True)
        # self.fields['ativo'].widget.attrs = {'class': 'form-control'}

class CampusForm(forms.ModelForm):
    class Meta:
        model = Campus
        fields = ('nome', 'descricao') 

    def __init__(self, *args, **kwargs):
        super(CampusForm, self).__init__(*args, **kwargs)
        self.fields['nome'].widget.attrs = {'class': 'form-control','placeholder':'Identificador do Campus'}
        self.fields['descricao'].widget.attrs = {'class': 'form-control','rows': 3, 'cols': 40, 'style':'resize:none','placeholder':'Informação extra'}

class FotoPredioForm(forms.ModelForm):
    class Meta:
        model = FotoPredio
        fields = ('foto',) 

    def __init__(self, *args, **kwargs):
        super(FotoPredioForm, self).__init__(*args, **kwargs)
        self.fields['foto'].widget.attrs = {'class': 'form-control-file'}
            
class SalaForm(forms.ModelForm):
    class Meta:
        model = Sala
        fields = ('identificador', 'predio',) 

    # labels = ({
    #             'qtd_tomas' : 'bancadas', 
    #             'qtd_computadores' : 'Computadores',
    #         })

    def __init__(self, *args, **kwargs):
        super(SalaForm, self).__init__(*args, **kwargs)
        self.fields['identificador'].widget.attrs = {'class': 'form-control','placeholder':'Número que identifique a sala'}
        self.fields['predio'].widget.attrs = {'class': 'form-control'}
        self.fields['predio'].queryset = Predio.objects.filter(ativo=True)

class EspacoForm(forms.ModelForm):
    class Meta:
        model = Espaco
        fields = ('identificador', 'descricao', 'sala', 'qtd_computadores', 'qtd_bancadas') 

    # labels = ({
    #             'qtd_tomas' : 'bancadas', 
    #             'qtd_computadores' : 'Computadores',
    #         })

    def __init__(self, *args, **kwargs):
        super(EspacoForm, self).__init__(*args, **kwargs)
        self.fields['identificador'].widget.attrs = {'class': 'form-control','placeholder':'Identificador do Espaço'}
        self.fields['descricao'].widget.attrs = {'class': 'form-control','rows': 3, 'cols': 40, 'style':'resize:none','placeholder':'Informação extra'}
        self.fields['sala'].widget.attrs = {'class': 'form-control'}
        self.fields['sala'].queryset = Sala.objects.filter(ativo=True)
        self.fields['qtd_bancadas'].widget.attrs = {'class': 'form-control'}
        self.fields['qtd_computadores'].widget.attrs = {'class': 'form-control'}

class FotoEspacoForm(forms.ModelForm):
    class Meta:
        model = FotoEspaco
        fields = ('foto',) 

    def __init__(self, *args, **kwargs):
        super(FotoEspacoForm, self).__init__(*args, **kwargs)
        self.fields['foto'].widget.attrs = {'class': 'form-control-file'}