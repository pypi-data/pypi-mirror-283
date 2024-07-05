from django.contrib.auth.decorators import login_required
from django.shortcuts import render


def home(request):
    ctx = {"user": request.user}
    return render(request, "example/home.html", ctx)


@login_required
def protected_page(request):
    return render(request, "example/protected.html")
