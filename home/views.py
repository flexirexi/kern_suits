from django.shortcuts import render


def index(request):
    """A view to return the index page"""
    return render(request, 'home/index.html')


def privacy(request):
    """A view to return the privacy policy page"""
    return render(request, 'home/privacy.html')


def about(request):
    """A view to return the about page"""
    return render(request, 'home/about.html')


def impressum(request):
    """A view to return the impressum page"""
    return render(request, 'home/impressum.html')


def terms_conditions(request):
    """A view to return the page of Terms & Conditions"""
    return render(request, 'home/terms_conditions.html')
