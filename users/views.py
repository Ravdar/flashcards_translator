from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import Profile

def register(request):
    if request.method == "POST":
        if 'username' in request.POST and 'password' in request.POST:
            # Log into guest account
            login_form = AuthenticationForm(request.POST)
            return redirect("mainapp:translator")
        else:
            # Register new account
            form = UserCreationForm(request.POST)
            if form.is_valid():
                new_user = form.save()
                Profile.objects.create(user=new_user)
                # login(request, new_user)
                return redirect("users:login")
    else:
        form = UserCreationForm()
        login_form = AuthenticationForm()
    return render(request, "registration/registration.html", {"form":form, "login_form":login_form})


