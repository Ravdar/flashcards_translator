from .models import Language

def create_language_objects(language_list):
    for lang_dict in language_list:
        Language.objects.create(
            name=lang_dict['name'],
            symbol=lang_dict['symbol']
        )


#MTRANSLATOR REFACTOR

# @login_required
# def translator(request):
#     """View for translation and adding flashcards."""
#     translator_form = TranslatorForm(request.user)
#     new_deck_form = NewDeck()
#     language_from, language_to = get_default_languages()
    
#     if request.method == "POST":
#         handle_post_request(request, new_deck_form)
    
#     if request.headers.get("x-requested-with") == "XMLHttpRequest":
#         return handle_ajax_request(request)
    
#     return render(request, "mainapp/translator.html", {
#         "translator_form": translator_form,
#         "new_deck_form": new_deck_form,
#         "language_from": language_from,
#         "language_to": language_to
#     })

# def get_default_languages():
#     language_from = get_object_or_404(Language, name="english")
#     language_to = get_object_or_404(Language, name="french")
#     return language_from, language_to

# def handle_ajax_request(request):
#     action = request.GET.get("action")
#     if action == "translate":
#         return handle_translation_request(request)
#     elif action == "change_language":
#         return change_language_flags(request)
#     return JsonResponse({"error": "Invalid action"}, status=400)

# def handle_translation_request(request):
#     input_text = request.GET.get("input_text")
#     is_flashcard = json.loads(request.GET.get("is_flashcard", "false"))
#     decks = json.loads(request.GET.get("decks", "[]"))
#     from_language = get_object_or_404(Language, name=request.GET.get("from_language"))
#     to_language = get_object_or_404(Language, name=request.GET.get("to_language"))

#     output_text = translate_text(input_text, from_language.symbol, to_language.symbol)
#     translation = Translation.objects.create(
#         input_text=input_text, output_text=output_text,
#         is_flashcard=is_flashcard, user=request.user,
#         from_language=from_language, to_language=to_language
#     )

#     if is_flashcard:
#         create_flashcards(input_text, output_text, decks, request.user, from_language, to_language)

#     return JsonResponse({"output_text": output_text})

# def translate_text(input_text, from_symbol, to_symbol):
#     # Placeholder for the actual translation logic
#     return f"Translated {input_text} from {from_symbol} to {to_symbol}"

# def create_flashcards(input_text, output_text, decks, user, from_language, to_language):
#     for deck_name in decks:
#         deck, created = Deck.objects.get_or_create(user=user, name=deck_name)
#         Flashcard.objects.create(
#             front=input_text, back=output_text,
#             user=user, deck=deck,
#             from_language=from_language, to_language=to_language
#         )

# def change_language_flags(request):
#     language_from = get_object_or_404(Language, name=request.GET.get("from_language"))
#     language_to = get_object_or_404(Language, name=request.GET.get("to_language"))
#     return JsonResponse({
#         "language_from_alpha2_code": language_from.alpha2_code,
#         "language_to_alpha2_code": language_to.alpha2_code
#     })

# def handle_post_request(request, new_deck_form):
#     if new_deck_form.is_bound and new_deck_form.is_valid():
#         new_deck = new_deck_form.save(commit=False)
#         new_deck.created_by = request.user
#         new_deck.user = request.user
#         new_deck.save()