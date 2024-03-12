from django import forms

from .models import Translation, Deck, Language

from django_select2 import forms as s2forms


class TranslatorForm(forms.ModelForm):
    def __init__(self, user, *args, **kwargs):
        super(TranslatorForm, self).__init__(*args, **kwargs)
        self.fields["decks"].queryset = Deck.objects.filter(user=user)
        self.fields["decks"].required = False
        self.fields["decks"].placeholder = "Select the decks you want to add the card"

        default_from_language = Language.objects.get(name="auto")
        default_to_language = Language.objects.get(name="english")
        self.fields['from_language'] = forms.ModelChoiceField(queryset=Language.objects.all(),initial=default_from_language)
        self.fields['to_language'] = forms.ModelChoiceField(queryset=Language.objects.exclude(name="auto"),initial=default_to_language)

    decks = forms.ModelMultipleChoiceField(queryset=Deck.objects.none(),widget=s2forms.Select2MultipleWidget(attrs={'data-placeholder': 'Select decks'}))

    class Meta:
        model = Translation
        fields = ["input_text", "is_flashcard","decks","from_language", "to_language"]


class NewDeck(forms.ModelForm):
    class Meta:
        model = Deck
        fields = ["name", "description"]