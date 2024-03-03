from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from .models import Profile

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            new_user = form.save()
            Profile.objects.create(user=new_user)
            # login(request, new_user)
            return redirect("users:login")
    else:
        form = UserCreationForm()
    return render(request, "registration/registration.html", {"form":form})


