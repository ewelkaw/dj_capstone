from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        # Handle user signup logic here
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect("project_list")
        else:
            return redirect("signup")
    else:
        form = UserCreationForm()
    return render(request, "accounts/signup.html", {"form": form})
