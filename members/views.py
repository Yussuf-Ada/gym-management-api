from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
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

    @action(detail=True, methods=['post'], parser_classes=[MultiPartParser, FormParser])
    def upload_image(self, request, pk=None):
        member = self.get_object()
        if 'profile_image' not in request.FILES:
            return Response({'error': 'No image provided'}, status=status.HTTP_400_BAD_REQUEST)
        
        print(f"Uploading image for member: {member.id}")
        print(f"Image file: {request.FILES['profile_image']}")
        
        member.profile_image = request.FILES['profile_image']
        member.save()
        
        print(f"Image saved. URL: {member.profile_image.url}")
        print(f"Image storage: {member.profile_image.storage}")
        
        return Response({'profile_image': member.profile_image.url})
