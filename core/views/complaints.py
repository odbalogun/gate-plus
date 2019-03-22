from rest_framework import status, viewsets
from rest_framework.response import Response
from core.serializers import ComplaintSerializer
from core.models import Complaints


class ComplaintViewSet(viewsets.ModelViewSet):
    serializer_class = ComplaintSerializer
    permission_classes = ()
    authentication_classes = ()
    queryset = Complaints.objects.all()
