from django.shortcuts import render
from .forms import TranslatorForm
import translators as ts

# Create your views here.
def translator(request):
    if request.method == "POST":
        print("POSTEDDDDD")
        translator_form = TranslatorForm(request.POST)
        if translator_form.is_valid():
            print("valid")
            input_text = translator_form.cleaned_data["input_text"]
            translated_text = ts.translate_text(input_text, to_language="en")
            print(translated_text)
            translator_form = TranslatorForm(initial={'output_text': translated_text})
    else:
            translator_form = TranslatorForm()
            print("GEEEETED")
    return render(request, "mainapp/translator.html", {"translator_form":translator_form})
