from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from .forms import TranslatorForm
from .models import Translation, Flashcard

import translators as ts

def landing_page(request):
     return render(request,"mainapp/landing_page.html", {})

@login_required
def translator(request):
    if request.method == "POST":
        translator_form = TranslatorForm(request.user,request.POST)
        if translator_form.is_valid():
            input_text = translator_form.cleaned_data["input_text"]
            translated_text = ts.translate_text(input_text, to_language="en")
            is_flashcard = translator_form.cleaned_data["is_flashcard"]
            translation = Translation(input_text=input_text, output_text=translated_text,is_flashcard=is_flashcard, user=request.user)
            translation.save()
            if is_flashcard:
                 flashcard = Flashcard(front=input_text, back=translated_text, user=request.user)
                 flashcard.save()
    else:
            translator_form = TranslatorForm(request.user)
            input_text = ""
            translated_text = ""
    return render(request, "mainapp/translator.html", {"translator_form":translator_form, "input_text":input_text, "translated_text":translated_text})
