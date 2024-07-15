from django.http import Http404
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response

from users.models import Profile
from users.serializers import UserSerializer


# Custom Auth class for desktop login
class APIAuth(ObtainAuthToken):
    permission_classes = ()
    serializer_class = AuthTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)
        upz = Profile.objects.filter(user=user).first()
        if upz:
            return Response({"user": UserSerializer(user).data, "token": token.key, "upazila": upz.upazila_code})
        else:
            # "Only upazilas can use BAHIS-desk"
            raise Http404
