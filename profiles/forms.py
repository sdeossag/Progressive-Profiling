from django import forms
from .models import Profile

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['career_goals', 'experience_level', 'skills', 'interests', 'values']
        widgets = {
            'career_goals': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Ej. Convertirme en líder de producto'}),
            'experience_level': forms.Select(attrs={'class': 'form-control'}),
            'skills': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Python, liderazgo'}),
            'interests': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. IA, diseño'}),
            'values': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ej. Innovación, ética'}),
        }
