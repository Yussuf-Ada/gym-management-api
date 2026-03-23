from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Member
from .serializers import MemberSerializer, MemberListSerializer
from .filters import MemberFilter


class MemberViewSet(viewsets.ModelViewSet):
    queryset = Member.objects.all()
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend, SearchFilter, OrderingFilter)
    filterset_class = MemberFilter
    search_fields = ('first_name', 'last_name', 'email', 'phone')
    ordering_fields = ('first_name', 'last_name', 'joined_date', 'created_at')
    ordering = ('-created_at',)

    def get_serializer_class(self):
        if self.action == 'list':
            return MemberListSerializer
        return MemberSerializer
