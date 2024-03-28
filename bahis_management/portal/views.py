import json

from authlib.integrations.django_client import OAuth
from django.conf import settings
from django.shortcuts import redirect, render
from django.urls import reverse

from config.settings.base import env

oauth = OAuth()
oauth.register(
    name="bahis_oidc",
    server_metadata_url=settings.OAUTH2_SERVER_METADATA_URL,
    client_kwargs={"scope": "openid email profile"},
)


def home(request):
    user = request.session.get("user")
    if user:
        user = json.dumps(user)

    kobo_url = env("KOBOTOOLBOX_URL")
    dash_url = env("BAHIS_DASHBOARD_URL")
    return render(request, "portal/home.html", context={"user": user, "kobo_url": kobo_url, "dash_url": dash_url})


def login(request):
    redirect_uri = request.build_absolute_uri(reverse("auth"))
    return oauth.bahis_oidc.authorize_redirect(request, redirect_uri)


def auth(request):
    token = oauth.bahis_oidc.authorize_access_token(request)
    request.session["user"] = token["userinfo"]
    return redirect("/")


def logout(request):
    request.session.pop("user", None)
    return redirect("/")
