from rest_framework import status, viewsets
from rest_framework.response import Response
from core.serializers import UserSerializer
from estates.models import Estate
from django.contrib.auth import get_user_model
from rest_framework.decorators import action

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = ()
    authentication_classes = ()
    queryset = User.objects.all()

    @action(detail=False, url_path='/signup/', methods=['POST'])
    def signup(self, request):
        data = request.data
        estate = data.pop('estate')

        if not estate:
            return Response({'detail': 'Estate must be provided'}, status=status.HTTP_400_BAD_REQUEST)

        # save estate
        e = Estate(name=estate)
        e.save()

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        # self.perform_create(serializer)
        serializer.save(estate=e)

        return Response(serializer.data, status=status.HTTP_201_CREATED)
