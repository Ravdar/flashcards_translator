from django.shortcuts import render
from .forms import TranslatorForm
import translators as ts

# Create your views here.
def translator(request):
    if request.method == "POST":
        translator_form = TranslatorForm(request.POST)
        if translator_form.is_valid():
            input_text = translator_form.cleaned_data["input_text"]
            translated_text = ts.translate_text(input_text, to_language="en")
    else:
            translator_form = TranslatorForm()
            input_text = ""
            translated_text = ""
    return render(request, "mainapp/translator.html", {"translator_form":translator_form, "input_text":input_text, "translated_text":translated_text})
