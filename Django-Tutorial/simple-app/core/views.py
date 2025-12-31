from django.shortcuts import render

def home(request):
    context = {
        "title": "Django Simple App",
        "message": "Welcome to Django!",
        "features": [
            "Built with Django 5.0",
            "Simple and clean structure",
            "Ready to extend"
        ]
    }
    return render(request, "home.html", context)
