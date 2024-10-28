from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.models import Group
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ObjectDoesNotExist




class RegisterSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=get_user_model().objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    groups = serializers.IntegerField(required=True)

    class Meta:
        model = get_user_model()
        fields = [
            "id",
            "first_name",
            "last_name",
            "password",
            "username",
            "groups"
        ]

    def create(self, validated_data):
        groups_data = validated_data.pop('groups', None)
        user = get_user_model().objects.create_user(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        if groups_data is not None:
            try:
                role = Group.objects.get(id=groups_data)
                user.groups.set([role])
            except ObjectDoesNotExist:
                raise serializers.ValidationError({'error': "Invalid role"})

        return user

    def update(self, instance, validated_data):
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        instance.username = validated_data.get('username', instance.username)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()
        return instance


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class IncorrectCredentialsError(serializers.ValidationError):
    pass


class UnverifiedAccountError(serializers.ValidationError):
    pass


class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=50, min_length=2)
    password = serializers.CharField(max_length=50, min_length=1)

    class Meta:
        model = get_user_model()
        fields = ("username", "password")

    def validate(self, data):
        username = data.get("username")
        password = data.get("password")
        user = self.authenticate_user(username, password)


        data["user"] = user
        return data

    def authenticate_user(self, username, password):
        return authenticate(username=username, password=password)


class UserPorfilesSerializers(serializers.ModelSerializer):
    groups = serializers.SerializerMethodField()

    class Meta:
        model = get_user_model()
        fields = ['id', 'first_name', 'last_name', 'username', 'groups']

    def get_groups(self, obj):
        return obj.groups.values('name')
