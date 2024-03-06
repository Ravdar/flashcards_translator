from django import forms
from .models import Translation, Deck

class TranslatorForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TranslatorForm, self).__init__(*args, **kwargs)
        self.fields['decks'].queryset = Deck.objects.filter(user=user)

    decks = forms.ModelMultipleChoiceField(queryset=Deck.objects.none())

    class Meta:
        model = Translation
        fields = ['input_text', 'is_flashcard','decks']