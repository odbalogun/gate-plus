from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from estates.models import Estate

User = get_user_model()


class EstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = ('id', 'name', 'slug', 'domain_url')
        extra_kwargs = {'domain_url': {'read_only': True}}


class SignupSerializer(serializers.ModelSerializer):
    estate = EstateSerializer(many=False, required=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone', 'email', 'password', 'estate')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        estate = validated_data.pop('estate')

        # save estate
        e = Estate.tenancy.create_estate(name=estate['name'], slug=estate['slug'])
        e.save()

        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.estate = e
        user.save()

        # create user token for rest authentication
        Token.objects.create(user=user)

        return user


