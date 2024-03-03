from django import forms
from .models import Translation

class TranslatorForm(forms.ModelForm):
    class Meta:
        model = Translation
        fields = ['input_text', "is_flashcard"]