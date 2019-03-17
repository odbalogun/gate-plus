from rest_framework import status, viewsets
from rest_framework.response import Response
from core.serializers import SignupSerializer
from estates.models import Estate
from django.db.models import Q
from django.contrib.auth import get_user_model
from rest_framework.decorators import action

User = get_user_model()


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

        # estate = request.data.pop('estate')
        # data = request.data
        #
        # if not estate:
        #     return Response({'detail': 'Estate must be provided'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # # check that estate params do not already exist
        # if Estate.objects.filter(Q(name=estate['name']) | Q(slug=estate['slug'])).exists():
        #     return Response({'detail': 'Estate name or slug already exist'}, status=status.HTTP_400_BAD_REQUEST)
        #
        # # save estate
        # e = Estate.tenancy.create_estate(name=estate['name'], slug=estate['slug'])
        # e.save()
        #
        # serializer = self.get_serializer(data=data)
        # serializer.is_valid(raise_exception=True)
        # # self.perform_create(serializer)
        # serializer.save(estate=e)
        #
        # return Response(serializer.data, status=status.HTTP_201_CREATED)
