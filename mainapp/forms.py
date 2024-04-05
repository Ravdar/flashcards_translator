from django import forms

from .models import Translation, Deck, Language

from django_select2 import forms as s2forms
from django_toggle_switch_widget.widgets import DjangoToggleSwitchWidget


class TranslatorForm(forms.ModelForm):
    """Form for creating translations and adding flashcards to the decks."""

    def __init__(self, user, *args, **kwargs):
        super(TranslatorForm, self).__init__(*args, **kwargs)
        self.fields["decks"].queryset = Deck.objects.filter(user=user)
        self.fields["decks"].required = False


        default_from_language = Language.objects.get(name="english")
        default_to_language = Language.objects.get(name="french")
        self.fields["from_language"] = forms.ModelChoiceField(queryset=Language.objects.exclude(name="auto"),initial=default_from_language)
        self.fields["to_language"] = forms.ModelChoiceField(queryset=Language.objects.exclude(name="auto"),initial=default_to_language)
        self.fields["is_flashcard"].widget = DjangoToggleSwitchWidget(round=True, klass="django-toggle-switch-success")

    decks = forms.ModelMultipleChoiceField(queryset=Deck.objects.none(),widget=s2forms.Select2MultipleWidget(attrs={'data-placeholder': 'Select decks'}))

    class Meta:
        model = Translation
        fields = ["input_text", "is_flashcard","decks","from_language", "to_language"]

class SearchDecks(forms.ModelForm):
    """Form for searching specific deck."""

    class Meta:
        model=Deck
        fields=["name"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.fields["name"].queryset = Deck.objects.filter(user=user)
        # self.fields["name"].required = False
        self.fields['name'].widget = s2forms.Select2MultipleWidget(attrs={'data-placeholder': 'Search for decks'})


class NewDeck(forms.ModelForm):
    """Form for creating a new deck."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["description"].widget = forms.Textarea(attrs={'cols':70,'rows':8})

    class Meta:
        model = Deck
        fields = ["name", "description"]
