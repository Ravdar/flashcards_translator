from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone

from .forms import TranslatorForm, NewDeck
from .models import Translation, Flashcard,Deck,Language

import translators as ts

def landing_page(request):
     return render(request,"mainapp/landing_page.html", {})

@login_required
def translator(request):
    if request.method == "POST":
        translator_form = TranslatorForm(request.user,request.POST)
        if translator_form.is_valid():
            # Get data from the form
            input_text = translator_form.cleaned_data["input_text"]
            from_language=Language.objects.get(name=translator_form.cleaned_data["from_language"])
            from_language_symbol = from_language.symbol
            to_language = Language.objects.get(name=translator_form.cleaned_data["to_language"])
            to_language_symbol = to_language.symbol            
            is_flashcard = translator_form.cleaned_data["is_flashcard"]
            decks = translator_form.cleaned_data["decks"]
            #Translate text and create Translation object
            translated_text = ts.translate_text(query_text=input_text, translator="google",from_language=from_language_symbol, to_language=to_language_symbol)
            translation = Translation(input_text=input_text, output_text=translated_text,is_flashcard=is_flashcard, user=request.user, from_language=from_language, to_language=to_language)
            translation.save()
            # Create Flashcard objects and manage all selected decks
            if is_flashcard:
                for deck in decks:
                    flashcard = Flashcard(front=input_text, back=translated_text,  user=request.user, deck=deck)
                    flashcard.save()
    # GET request               
    else:
        translator_form = TranslatorForm(request.user)
        input_text = ""
        translated_text = ""
    return render(request, "mainapp/translator.html", {"translator_form":translator_form, "input_text":input_text, "translated_text":translated_text})

def study(request, deck_name):
    deck = get_object_or_404(Deck, name=deck_name)




def user_profile(request, user_username):
    user = get_object_or_404(User, username=user_username)
    if request.method == "POST":
        new_deck_form = NewDeck(request.POST)
        if new_deck_form.is_valid():
            new_deck = new_deck_form.save(commit=False)
            new_deck.created_by = request.user
            new_deck.save()
            new_deck.user.add(request.user)
            new_deck.save()
            new_deck_form= NewDeck()
    else: 
        new_deck_form= NewDeck()
    return render(request, "mainapp/user_profile.html", {"user":user, "new_deck_form":new_deck_form})

