from django.shortcuts import render

# Create your views here.
def translator(request):
    return render(request, "mainapp/translator.html",)
