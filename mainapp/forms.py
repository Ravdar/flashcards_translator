from django import forms
from .models import Translation

class TranslatorForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ['input_text', 'output_text']
        widgets = {
            'input_text': forms.Textarea(attrs={'rows': 4, 'cols': 40}),
            'output_text': forms.Textarea(attrs={'rows': 4, 'cols': 40, 'readonly': 'readonly'})
        }