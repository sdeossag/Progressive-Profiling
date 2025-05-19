# forms.py

from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['objetivos_profesionales', 'categoria_trabajo', 'nivel_experiencia', 'habilidades', 'intereses', 'valores', 
                  'educacion_maxima', 'certificaciones', 'tipo_trabajo_preferido', 'disponibilidad', 'idiomas_hablados']
        widgets = {
            'objetivos_profesionales': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ej. Convertirme en líder de producto'}),
            'categoria_trabajo': forms.Select(attrs={'class': 'form-control'}),
            'nivel_experiencia': forms.Select(attrs={'class': 'form-control'}),
            'habilidades': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Python, liderazgo'}),
            'intereses': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. IA, diseño'}),
            'valores': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Innovación, ética'}),
            'educacion_maxima': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Licenciatura, Maestría'}),
            'certificaciones': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ej. Certificación en Scrum'}),
            'tipo_trabajo_preferido': forms.Select(attrs={'class': 'form-control'}),
            'disponibilidad': forms.Select(attrs={'class': 'form-control'}),
            'idiomas_hablados': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Inglés, Español'}),
        }

