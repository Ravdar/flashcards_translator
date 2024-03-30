from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .forms import TranslatorForm, NewDeck, SearchDecks
from .models import Translation, Flashcard,Deck,Language
from users.models import Profile

from contributions_django.graphs import generate_contributors_graph
import translators as ts
import random
import time
from datetime import timedelta
from django.utils import timezone

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
        end_time = int(time.time() * 1000)
        print(end_time)
        start_time = int(request.GET.get("start_time"))
        quality = int(request.GET.get("quality"))
        previous_card_id = int(request.GET.get("id"))
        previous_card = get_object_or_404(Flashcard, pk=previous_card_id)
        previous_card.total_time += (end_time-start_time)/1000
        previous_card.review_flashcard(quality)
        if quality == 3:
            previous_card.number_of_easy += 1
        elif quality == 2:
            previous_card.number_of_good += 1
        elif quality == 1:
            previous_card.number_of_hard +=1
        elif quality == 0:
            previous_card.number_of_agains +=1
        
        previous_card.save()
        # Retrieve deck, cards for review and shuffle it
        deck_name = request.GET.get("deck_name")
        deck = get_object_or_404(Deck, name=deck_name, user=request.user)
        flashcards_for_review = deck.flashcards_to_review()
        flashcards_list = list(flashcards_for_review)
        start_time = int(time.time() * 1000) 
        # Send next card for review if there are any
        if flashcards_list != []:
            random.shuffle(flashcards_list)
            next_card = flashcards_list[0]
            return JsonResponse({"front":next_card.front, "back":next_card.back, "id":next_card.id, "start_time":start_time})
        else:
            return JsonResponse({"id":"no more cards"})
    
    else:
        # Initial call and deck shuffle
        deck_name = request.GET.get("deck_name")
        deck = get_object_or_404(Deck, name=deck_name, user=request.user)
        flashcards_for_review = deck.flashcards_to_review()
        flashcards_list = list(flashcards_for_review)
        start_time = int(time.time() * 1000) 
        random.shuffle(flashcards_list)

    print(start_time)

    return render(request, "mainapp/review.html", {"deck_name":deck_name,"flashcards_list":flashcards_list,"start_time":start_time})


@login_required
def user_profile(request, user_username):
    """View for user profile and managing decks."""

    # Assign user
    user = get_object_or_404(User, username=user_username)
    all_user_decks = Deck.objects.filter(user=user)
    user_profile = get_object_or_404(Profile, user=user)

    # Overall stats
    decks_to_review = [deck for deck in all_user_decks if deck.has_flashcards_to_review]
    total_decks_reviewed_today = user_profile.total_decks_reviewed_today
    total_cards_reviewed_today = user_profile.total_flashcards_reviewed_today
    total_decks_to_review_today = len(decks_to_review)
    total_cards_to_review_today = user_profile.total_flashcards_to_review_today
    activity_streak = user_profile.activity_streak

    # Stats for specific deck
    decks_data =[]
    for deck in decks_to_review:
        number_of_flashcards_to_review = deck.flashcards_to_review().count()
        number_of_flashcards_reviewed_today = deck.number_of_flashcards_reviewed_today
        decks_data.append({
            "deck":deck,"number_of_flashcards_to_review":number_of_flashcards_to_review, "number_of_flashcards_reviewed_today":number_of_flashcards_reviewed_today})
        
    # Contributions calendar
    today = timezone.now()
    last_week = today - timedelta(days=7)
    contributions = []
    calendar = generate_contributors_graph(contributions, title="Decks reviews")
        
    return render(request, "mainapp/user_profile.html", {"user":user,"decks_data":decks_data,"total_decks_reviewed_today":total_decks_reviewed_today,"total_cards_reviewed_today":total_cards_reviewed_today, "total_cards_to_review_today":total_cards_to_review_today, "total_decks_to_review_today":total_decks_to_review_today,"calendar":calendar, "activity_streak":activity_streak}, )


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