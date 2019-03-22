from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.serializers import AuthTokenSerializer
from core.serializers import SignupSerializer
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from django.conf import settings
import datetime


User = get_user_model()
EXPIRE_HOURS = getattr(settings, 'REST_FRAMEWORK_TOKEN_EXPIRE_HOURS', 24)


class LoginView(ObtainAuthToken):
    def post(self, request, **kwargs):
        serializer = AuthTokenSerializer(data=request.data)

        if serializer.is_valid():
            token, created = Token.objects.get_or_create(user=serializer.validated_data['user'])
            if not created and token.created < datetime.datetime.now() - datetime.timedelta(hours=EXPIRE_HOURS):
                token.delete()
                token = Token.objects.create(user=serializer.validated_data['user'])
                token.created = datetime.datetime.now()
                token.save()

            if token.user.estate:
                return Response({
                                    "auth_token": token.key, "id": token.user.pk, "first_name": token.user.first_name,
                                    "last_name": token.user.last_name, "role": token.user.role,
                                    "expiry_date": token.created + datetime.timedelta(hours=EXPIRE_HOURS),
                                    "estate": {
                                        "id": token.user.estate.pk,
                                        "name": token.user.estate.name,
                                        "domain_url": token.user.estate.domain_url}
                                 }, status=status.HTTP_200_OK)
            else:
                return Response({"auth_token": token.key, "estate": token.user.estate, "id": token.user.pk,
                                 "role": token.user.role, "last_name": token.user.last_name,
                                 "first_name": token.user.first_name,
                                 'expiry_date': token.created + datetime.timedelta(hours=EXPIRE_HOURS)},
                                status=status.HTTP_200_OK)
        return Response({"error": "Invalid Credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = SignupSerializer
    permission_classes = ()
    authentication_classes = ()
    queryset = User.objects.all()

    @action(detail=False, methods=['post'])
    def signup(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
