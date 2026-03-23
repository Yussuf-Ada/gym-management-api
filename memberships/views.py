from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Membership
from .serializers import MembershipSerializer


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    permission_classes = (IsAuthenticated,)
    filterset_fields = ('is_active',)
    search_fields = ('name',)
    ordering_fields = ('name', 'price', 'duration_days')
    ordering = ('price',)
