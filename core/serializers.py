from rest_framework import serializers
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from estates.models import Estate

User = get_user_model()


class EstateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Estate
        fields = ('id', 'name')


class UserSerializer(serializers.ModelSerializer):
    estate_id = serializers.PrimaryKeyRelatedField(many=False, read_only=True, queryset=Estate.objects.all())
    estate = EstateSerializer(many=False, read_only=True)

    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'phone_number', 'email', 'password', 'estate', 'estate_id')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)

        user.set_password(validated_data['password'])
        user.save()

        # create user token for rest authentication
        # Token.objects.create(user=user)
        return user

