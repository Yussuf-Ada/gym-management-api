from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Membership, MemberMembership
from .serializers import MembershipSerializer, MemberMembershipSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('is_active',)
    search_fields = ('name',)
    ordering_fields = ('name', 'price', 'duration_days')
    ordering = ('price',)


class MemberMembershipViewSet(viewsets.ModelViewSet):
    queryset = MemberMembership.objects.select_related('member', 'membership').all()
    serializer_class = MemberMembershipSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('status', 'member', 'membership')
    ordering_fields = ('start_date', 'end_date', 'created_at')
    ordering = ('-start_date',)
