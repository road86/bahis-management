import base64
import hashlib
import random
import string

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from requests_oauthlib import OAuth2Session

oauth = settings.AUTHLIB_OAUTH_CLIENTS["bahis_oidc"]
scope = ["openid", "email", "profile", "introspection"]
# scope = ['read', 'write',]
token_url = oauth["token_url"]
client_secret = oauth["client_secret"]
user_info_url = oauth["user_info_url"]
authorization_base_url = oauth["authorization_base_url"]
client = OAuth2Session(client_id=oauth["client_id"], scope=scope)
code_verifier = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))

code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8").replace("=", "")


@login_required()
def home(request):
    user = request.user
    return render(request, "portal/home.html", context={"user": user})


def login(request):
    authorization_url, state = client.authorization_url(
        authorization_base_url, code_challenge=code_challenge, code_challenge_method="S256"
    )

    request.session["oauth_state"] = state
    return redirect(authorization_url)


def callback(request):
    token = client.fetch_token(
        token_url,
        client_secret=client_secret,
        authorization_response=request.build_absolute_uri(),
        code_verifier=code_verifier,
    )
    request.session["oauth_token"] = token
    request.session["access_token"] = token["access_token"]
    res = client.get(user_info_url)
    if res.status_code != 200:
        return HttpResponse(res.content)
    request.session["user"] = res.json()
    return redirect("/")


def profile(request):
    token = dict(request.session["access_token"])
    client.token = token
    res = client.get(user_info_url)
    return JsonResponse(
        {"home": settings.OAUTH2_SERVER_URL, "profile": res.json(), "token": request.session["access_token"]}
    )


def logout(request):
    request.session.pop("user", None)
    request.session.pop("oauth_token", None)
    request.session.pop("access_token", None)
    return redirect("/")
