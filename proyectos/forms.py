from django import forms
from django.forms import widgets
from .models import Proyecto, Pago, Documento, Imagen, Cambio, Actividad

class ProyectoForm(forms.ModelForm):
    class Meta:
        model = Proyecto
        fields = ['nombre', 'objeto', 'contratista', 'numero_contrato', 'valor_proyecto','estado', 'fecha_inicio', 'fecha_fin', 'responsable', 'interventoria','terminal', 'programado', 'avance']
        widgets = {
            'fecha_inicio':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'}),
            'fecha_fin':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'})
        }


class PagoForm(forms.ModelForm):
    class Meta:
        model = Pago
        fields = ['proyecto', 'valor_pago', 'fecha_pago', 'numero_factura','concepto_pago']
        widgets = {
            'fecha_pago':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'}),
        }


class DocumentoForm(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['proyecto', 'nombre', 'documento']
        # widgets = {
        #     'documento':forms.FileInput(),
        # }


class ImagenForm(forms.ModelForm):
    class Meta:
        model = Imagen
        fields = ['proyecto', 'nombre', 'imagen']


class CambioForm(forms.ModelForm):
    class Meta:
        model = Cambio
        fields = ['proyecto', 'tipo', 'afecta_tiempo', 'duracion', 'afecta_costo', 'costo', 'fecha_de_cambio', 'genero_documento', 'nombre_documento']
        widgets = {
            'fecha_de_cambio':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'})
        }


class ActividadForm(forms.ModelForm):
    class Meta:
        model = Actividad
        fields = ['proyecto', 'nombre', 'fecha_inicio', 'fecha_fin','programado', 'avance']
        widgets = {
            'fecha_inicio':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'}),
            'fecha_fin':forms.DateInput(attrs={'placeholder':'dd/mm/aaaa'})
        }