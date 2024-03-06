from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import TranslatorForm
from .models import Translation, Flashcard,Deck

import translators as ts

def landing_page(request):
     return render(request,"mainapp/landing_page.html", {})

@login_required
def translator(request):
    if request.method == "POST":
        translator_form = TranslatorForm(request.user,request.POST)
        if translator_form.is_valid():
            print("valid")
            input_text = translator_form.cleaned_data["input_text"]
            translated_text = ts.translate_text(input_text, to_language="en")
            is_flashcard = translator_form.cleaned_data["is_flashcard"]
            translation = Translation(input_text=input_text, output_text=translated_text,is_flashcard=is_flashcard, user=request.user)
            translation.save()
            if is_flashcard:
                flashcard = Flashcard(front=input_text, back=translated_text,  user=request.user)
                flashcard.save()
                decks = translator_form.cleaned_data["decks"]
                if not decks.exists():
                    unnamed_deck = Deck.objects.filter(name="Unnamed deck")
                    if not unnamed_deck.exists():
                        unnamed_deck = Deck(name="Unnamed deck", created_by=request.user)
                        unnamed_deck.save()
                        unnamed_deck.user.add(request.user)
                        unnamed_deck.save()
                        flashcard.decks.add(unnamed_deck)
                    else:
                        flashcard.decks.set(unnamed_deck)
                else:
                    flashcard.decks.set(decks)
                flashcard.save()
        else:
            print("invalid")
    else:
        translator_form = TranslatorForm(request.user)
        input_text = ""
        translated_text = ""
    return render(request, "mainapp/translator.html", {"translator_form":translator_form, "input_text":input_text, "translated_text":translated_text})
