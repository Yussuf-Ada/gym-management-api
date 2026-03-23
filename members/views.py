from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Member
from .serializers import MemberSerializer, MemberListSerializer


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    permission_classes = (IsAuthenticated,)

    def get_serializer_class(self):
        if self.action == 'list':
            return MemberListSerializer
        return MemberSerializer
