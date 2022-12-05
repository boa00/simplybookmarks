from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request, "main_app/home_page.html")


def register_page(request):
    return render(request, "main_app/register_page.html")
    