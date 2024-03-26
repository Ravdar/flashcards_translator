from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import TranslatorForm, NewDeck, SearchDecks
from .models import Translation, Flashcard,Deck,Language

import translators as ts
import random

def landing_page(request):
     """View for landing page."""

     return render(request,"mainapp/landing_page.html", {})


@login_required
def translator(request):
    """View for translatation and adding flashcards."""

    if request.method == "POST":
        translator_form = TranslatorForm(request.user,request.POST)
        if translator_form.is_valid():
            # Retrieve data from the form
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
        else:
            print("invalid")            
    # GET request               
    else:
        translator_form = TranslatorForm(request.user)
        input_text = ""
        translated_text = ""

    return render(request, "mainapp/translator.html", {"translator_form":translator_form, "input_text":input_text, "translated_text":translated_text})


@login_required
def review(request):
    """View for deck review."""

    # Displaying next card, handled by AJAX request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Update reviewed card based on selected quality
        quality = int(request.GET.get("quality"))
        previous_card_id = int(request.GET.get("id"))
        previous_card = get_object_or_404(Flashcard, pk=previous_card_id)
        previous_card.review_flashcard(quality)
        previous_card.save()
        # Retrieve deck, cards for review and shuffle it
        deck_name = request.GET.get("deck_name")
        deck = get_object_or_404(Deck, name=deck_name, user=request.user)
        flashcards_for_review = deck.flashcards_to_review()
        flashcards_list = list(flashcards_for_review)
        # Send next card for review if there are any
        if flashcards_list != []:
            random.shuffle(flashcards_list)
            next_card = flashcards_list[0]
            return JsonResponse({"front":next_card.front, "back":next_card.back, "id":next_card.id})
        else:
            return JsonResponse({"id":"no more cards"})
    
    else:
        # Initial call and deck shuffle
        deck_name = request.GET.get("deck_name")
        deck = get_object_or_404(Deck, name=deck_name, user=request.user)
        flashcards_for_review = deck.flashcards_to_review()
        flashcards_list = list(flashcards_for_review)
        random.shuffle(flashcards_list)

    return render(request, "mainapp/review.html", {"deck_name":deck_name,"flashcards_list":flashcards_list})


@login_required
def user_profile(request, user_username):
    """View for user profile and managing decks."""

    # Assign user
    user = get_object_or_404(User, username=user_username)
    return render(request, "mainapp/user_profile.html", {"user":user,})


@login_required
def decks(request):
    """View for managing decks in user panel."""

    # Assign user
    user = request.user
    if request.method == "POST":
        # Handling form for adding new deck
        new_deck_form = NewDeck(request.POST)
        decks_searchbar = SearchDecks(request.POST)
        if new_deck_form.is_valid():
            new_deck = new_deck_form.save(commit=False)
            new_deck.created_by = request.user
            new_deck.save()
            new_deck.user.add(request.user)
            new_deck.save()
            new_deck_form= NewDeck()
    else:
        # GET request 
        new_deck_form= NewDeck()
        decks_searchbar = SearchDecks()
    return render(request, "mainapp/decks.html", {"user":user, "new_deck_form":new_deck_form,"decks_searchbar":decks_searchbar})