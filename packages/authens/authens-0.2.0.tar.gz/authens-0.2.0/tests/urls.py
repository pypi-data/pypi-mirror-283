from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.urls import include, path

# ---
# Two tiny views to easily test user authentication.
# ---


def public_view(request):
    return HttpResponse("OK")


@login_required
def private_view(request):
    return HttpResponse("OK")


# ---
# Urls: expose authens' urls + the above views.
# ---


urlpatterns = [
    path("public", public_view),
    path("private", private_view),
    path("authens/", include("authens.urls")),
]
