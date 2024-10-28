from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponsePermanentRedirect
from django.shortcuts import get_object_or_404
from django.core.serializers import serialize
from django.shortcuts import render,redirect
from django.contrib.auth.models import *
from django.forms.models import model_to_dict
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken
from rest_framework import generics, permissions, status, views
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
import collections, functools, operator
from authentification.renderers.renderers import UserRenderers
from authentification.serializer.serializer import RegisterSerializer, LoginSerializer, UserPorfilesSerializers
from main_services.expected_fields import check_required_key
from main_services.responses import bad_request_response, success_created_response, success_response, \
    unauthorized_response, success_deleted_response
from main_services.swaggers import swagger_extend_schema, swagger_schema


def get_token_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token)
    }


@swagger_extend_schema(fields={"first_name", "last_name", "username", "password"}, description="Register")
@swagger_schema(serializer=RegisterSerializer)
class RegisterView(APIView):
    def post(self, request):
        valid_fields = {"first_name", "last_name", "username", "password", "groups"}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = RegisterSerializer(data=request.data, context={'request': request})
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            return success_created_response(get_token_for_user(user))
        return bad_request_response(serializer.errors)


@swagger_extend_schema(fields={"username", "password"}, description="Login")
@swagger_schema(serializer=LoginSerializer)
class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        expected_fields = {"username", "password"}
        received_fields = set(request.data.keys())
        unexpected_fields = received_fields - expected_fields

        if unexpected_fields:
            return bad_request_response(
                f"Unexpected fields: {', '.join(unexpected_fields)}"
            )

        serializer = self.get_serializer(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        token = self.generate_user_token(user)

        return success_response(token)

    def get_serializer(self, *args, **kwargs):
        return LoginSerializer(*args, **kwargs)

    def generate_user_token(self, user):
        return get_token_for_user(user)


class ProfileView(APIView):
    permission_classes = [IsAuthenticated]
    render_classes = [UserRenderers]

    def get(self, request):
        if not request.user.is_authenticated:
            return unauthorized_response("Token is not valid")

        serializer = UserPorfilesSerializers(request.user, context={'request': request})
        return success_response(serializer.data)

    def put(self, request):
        if not request.user.is_authenticated:
            return unauthorized_response("Token is not valid")

        valid_fields = {'first_name', 'last_name', 'username', 'password'}
        unexpected_fields = check_required_key(request, valid_fields)
        if unexpected_fields:
            return bad_request_response(f"Unexpected fields: {', '.join(unexpected_fields)}")

        serializer = RegisterSerializer(instance=request.user, data=request.data, partial=True,
                                              context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return success_response(serializer.data)
        return bad_request_response(serializer.errors)

    def delete(self, request):
        if not request.user.is_authenticated:
            return unauthorized_response("Token is not valid")
        request.user.delete()
        return success_deleted_response("User deleted")