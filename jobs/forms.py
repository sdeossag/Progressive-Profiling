from django import forms
from .models import Job

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        # Excluimos campos que no deben editarse manualmente
        exclude = ['created_by', 'fecha_publicacion']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'habilidades_requeridas': forms.Textarea(attrs={'rows': 3}),
        }
