from django.shortcuts import render

from .forms import NewUserForm

# Create your views here.
def home_page(request):
    return render(request, "main_app/home_page.html")


def register_page(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
    return render(request, "main_app/register_page.html")


def login_page(request):
    return render(request, "main_app/login_page.html")
