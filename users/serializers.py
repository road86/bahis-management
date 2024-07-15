from django.contrib.auth.models import User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField("get_full_name")

    def get_full_name(self, _user):
        return _user.first_name + " " + _user.last_name

    class Meta:
        model = User
        fields = ("id", "password", "username", "name", "email")
