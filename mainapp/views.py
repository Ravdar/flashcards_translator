from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

from .forms import TranslatorForm, NewDeck
from .models import Translation, Flashcard,Deck,Language
from users.models import Profile

import translators as ts
import json
import random
import time
from datetime import datetime
from contributions_django.graphs import generate_contributors_graph

def landing_page(request):
     """View for landing page."""

     return render(request,"mainapp/landing_page.html", {})


@login_required
def translator(request):
    """View for translatation and adding flashcards."""

    # Passing initial parameters (needed for all requests)
    new_deck_form= NewDeck()
    translator_form = TranslatorForm(request.user)
    input_text = ""
    output_text = ""
    # Default set languages needed for displaying flags
    language_from = get_object_or_404(Language, name="english")
    language_to = get_object_or_404(Language, name="french")
    if request.method == "GET":
        # Handling AJAX request
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            print("ajax")
            action = request.GET.get("action")
            # Recognise what kind of AJAX request is it
            if action == "translate":
                # Retrieve data from AJAX request
                input_text = request.GET.get("input_text")
                is_flashcard = request.GET.get("is_flashcard")
                decks_string = request.GET.get("decks")
                from_language = Language.objects.get(name=request.GET.get("from_language"))
                to_language = Language.objects.get(name=request.GET.get("to_language"))
                # Transform retrieved data
                if is_flashcard == "true":
                    is_flashcard = True
                else:
                    is_flashcard = False
                decks = json.loads(decks_string)
                from_language_symbol = from_language.symbol
                to_language_symbol = to_language.symbol
                # #Translate text and create Translation object
                output_text = ts.translate_text(query_text=input_text, translator="google",from_language=from_language_symbol, to_language=to_language_symbol)
                translation = Translation(input_text=input_text, output_text=output_text,is_flashcard=is_flashcard, user=request.user, from_language=from_language, to_language=to_language)
                translation.save()
                # Create Flashcard objects and manage all selected decks
                if is_flashcard:
                    for deck_name in decks:
                        deck = get_object_or_404(Deck, user=request.user, name=deck_name)
                        flashcard = Flashcard(front=input_text, back=output_text,  user=request.user, deck=deck, from_language=from_language, to_language=to_language)
                        flashcard.save()
                return JsonResponse({"output_text":output_text})
            else:
                # Change country flag
                language_from_string = request.GET.get("from_language_string")
                language_to_string = request.GET.get("to_language_string")
                language_from = get_object_or_404(Language, name=language_from_string)
                language_to = get_object_or_404(Language, name=language_to_string)
                language_from_alpha2_code = language_from.alpha2_code
                language_to_alpha2_code = language_to.alpha2_code
                return JsonResponse({"language_from_alpha2_code":language_from_alpha2_code, "language_to_alpha2_code":language_to_alpha2_code})
        else:
            # If it is requested from 'Add flashcard' button in deck_details view
            if request.GET.get("requested_from") == "deck_details":
                deck_name = request.GET.get("deck_name")
                deck = Deck.objects.filter(user=request.user, name=deck_name)
                translator_form = TranslatorForm(request.user, initial={"is_flashcard":True, "decks":deck})
                input_text = ""
                output_text = ""
    else:
        # POST request
        # Handling form for adding new deck
            new_deck_form = NewDeck(request.POST)
            if new_deck_form.is_valid():
                new_deck = new_deck_form.save(commit=False)
                new_deck.created_by = request.user
                new_deck.user = request.user
                new_deck.save()

    return render(request, "mainapp/translator.html", {"translator_form":translator_form, "input_text":input_text, "output_text":output_text, "new_deck_form":new_deck_form, "language_from":language_from, "language_to":language_to} )
    

@login_required
def edit_flashcard(request):
    """Editing flashcard in translator view"""

    if request.method == "POST":
        # Delete flashcard
        card_id = request.POST.get("card_id")
        card = get_object_or_404(Flashcard, pk=card_id)
        card.delete()
        url = reverse("mainapp:user_profile", kwargs={"user_username": request.user.username})
        # Redirect to the generated URL using HttpResponseRedirect
        return redirect(url)
    else:
        # Handling AJAX request
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            action = request.GET.get("action")
            # Recognise what kind of AJAX request is it
            if action == "edit":
                # Retrieve data from AJAX request
                card_id = request.GET.get("card_id")
                input_text = request.GET.get("input_text")
                output_text = request.GET.get("output_text")
                from_language = Language.objects.get(name=request.GET.get("from_language"))
                to_language = Language.objects.get(name=request.GET.get("to_language"))
                # Update flashcard object
                flashcard = get_object_or_404(Flashcard, pk=card_id)
                flashcard.front = input_text
                flashcard.back = output_text
                flashcard.from_language = from_language
                flashcard.to_language = to_language
                flashcard.save()
                return JsonResponse({})    
            else:
                # Change country flag
                language_from_string = request.GET.get("from_language_string")
                language_to_string = request.GET.get("to_language_string")
                language_from = get_object_or_404(Language, name=language_from_string)
                language_to = get_object_or_404(Language, name=language_to_string)
                language_from_alpha2_code = language_from.alpha2_code
                language_to_alpha2_code = language_to.alpha2_code
                return JsonResponse({"language_from_alpha2_code":language_from_alpha2_code, "language_to_alpha2_code":language_to_alpha2_code})                     
        else:
            # Initial GET request
            card_id = request.GET.get("card_id")
            card = get_object_or_404(Flashcard, pk = card_id)
            deck = card.deck
            card_front = card.front
            card_back = card.back
            from_language = card.from_language
            to_language = card.to_language
            translator_form = TranslatorForm(request.user, initial={"is_flashcard":True, "decks":deck,"from_language":from_language, "to_language":to_language})

        return render(request, "mainapp/edit_flashcard.html",{"card_id":card_id,"translator_form":translator_form, "input_text":card_front, "output_text":card_back, "card":card})


@login_required
def review(request):
    """View for deck review."""

    # Displaying next card, handled by AJAX request
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        # Update reviewed card based on selected quality
        end_time = int(time.time() * 1000)
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
    user_profile = get_object_or_404(Profile, user=user)
    activity_string = list(user_profile.activity)
    activity = [datetime.strptime(date, "%Y-%m-%d") for date in activity_string]
    print(activity)
    calendar = generate_contributors_graph(activity, title="")
        
    return render(request, "mainapp/user_profile.html", {"user":user,"decks_data":decks_data,"total_decks_reviewed_today":total_decks_reviewed_today,"total_cards_reviewed_today":total_cards_reviewed_today, "total_cards_to_review_today":total_cards_to_review_today, "total_decks_to_review_today":total_decks_to_review_today,"calendar":calendar, "activity_streak":activity_streak}, )


@login_required
def decks(request):
    """View for managing decks in user panel."""

    # Assign user
    user = request.user
    if request.method == "POST":
        # Handling form for adding new deck
            new_deck_form = NewDeck(request.POST)
            if new_deck_form.is_valid():
                new_deck = new_deck_form.save(commit=False)
                new_deck.created_by = request.user
                new_deck.user = request.user
                new_deck.save()
                new_deck_form= NewDeck()
    else:
    # AJAX request - decks filtering/search
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            search_text = request.GET.get("search_text")
            filtered_decks = Deck.objects.filter(user=user, name__icontains=search_text)
            # Retrieving only names, so it can be passed in JsonResponse
            filtered_decks_names = []
            for deck in filtered_decks:
                filtered_decks_names.append(deck.name)
            return JsonResponse({"filtered_decks":filtered_decks_names})
        else:
        # Regular GET request
            new_deck_form= NewDeck()
    return render(request, "mainapp/decks.html", {"user":user, "new_deck_form":new_deck_form,})

@login_required
def deck_details(request):
    """Browsing all flashcards inside a specific deck and other deck details."""
    
    user = request.user
    if request.method == "POST":
        deck_id = request.POST.get("deck_id")
        deck = get_object_or_404(Deck, pk=deck_id)
        deck.delete()
        url = reverse("mainapp:user_profile", kwargs={"user_username": request.user.username})
        # Redirect to the generated URL using HttpResponseRedirect
        return redirect(url)

    else:    
        deck_name = request.GET.get("deck_name")
        if request.headers.get("x-requested-with") == "XMLHttpRequest":
            search_text = request.GET.get("search_text")
            filtered_cards = Flashcard.objects.filter(user=user, front__icontains=search_text)
            filtered_cards_fronts = []
            for card in filtered_cards:
                filtered_cards_fronts.append(card.front)
            return JsonResponse({"filtered_cards":filtered_cards_fronts})
    deck = get_object_or_404(Deck,user=user,name=deck_name)
    return render(request, "mainapp/deck_details.html", {"deck":deck})


def hello_visitor(request):
    """View for no exisitng/upcoming functionalities and buttons."""

    return render(request,"mainapp/hello_visitor.html", {})