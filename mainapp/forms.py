from django import forms
from .models import Translation, Deck, Language

class TranslatorForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TranslatorForm, self).__init__(*args, **kwargs)
        self.fields["decks"].queryset = Deck.objects.filter(user=user)
        self.fields["decks"].required = False
        self.fields['from_language'] = forms.ModelChoiceField(queryset=Language.objects.all())
        self.fields['to_language'] = forms.ModelChoiceField(queryset=Language.objects.exclude(name="auto"))

    decks = forms.ModelMultipleChoiceField(queryset=Deck.objects.none(),widget=forms.CheckboxSelectMultiple)

    class Meta:
        model = Translation
        fields = ["input_text", "is_flashcard","decks","from_language", "to_language"]


class NewDeck(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ["name", "description"]