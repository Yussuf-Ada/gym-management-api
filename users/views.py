from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.db.models import Count, Q

from .serializers import UserSerializer, RegisterSerializer, LoginSerializer, UserProfileSerializer, ChangePasswordSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
from .models import PasswordResetToken
from .utils import send_password_reset_email

User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            'message': 'User created successfully. Please log in.',
            'user': UserSerializer(user).data
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        email = serializer.validated_data['email']
        password = serializer.validated_data['password']
        
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.check_password(password):
            return Response(
                {'error': 'Invalid credentials'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        if not user.is_active:
            return Response(
                {'error': 'Account is disabled'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        
        refresh = RefreshToken.for_user(user)
        return Response({
            'user': UserSerializer(user).data,
            'tokens': {
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }
        })


class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token:
                token = RefreshToken(refresh_token)
                token.blacklist()
            return Response({'message': 'Logged out successfully'}, status=status.HTTP_200_OK)
        except Exception:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user


class ChangePasswordView(APIView):
    permission_classes = (IsAuthenticated,)

    def put(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Incorrect password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password updated successfully'})


class DashboardStatsView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from members.models import Member
        from memberships.models import MemberMembership
        from classes.models import GymClass, ClassBooking

        today = timezone.now().date()
        user = request.user

        # Check if user is admin - use OR condition for flexibility
        if user.role == 'admin' or user.is_staff:
            # Admin sees all data
            total_members = Member.objects.filter(is_active=True).count()
            active_subscriptions = MemberMembership.objects.filter(
                status='active',
                end_date__gte=today
            ).count()
            expiring_soon = MemberMembership.objects.filter(
                status='active',
                end_date__gte=today,
                end_date__lte=today + timezone.timedelta(days=7)
            ).count()
            total_classes = GymClass.objects.filter(is_active=True).count()
            todays_bookings = ClassBooking.objects.filter(
                booking_date=today,
                status='confirmed'
            ).count()
        else:
            # Regular users see their own data (empty for new users)
            total_members = 0
            active_subscriptions = 0
            expiring_soon = 0
            total_classes = 0
            todays_bookings = 0

        return Response({
            'total_members': total_members,
            'active_subscriptions': active_subscriptions,
            'expiring_soon': expiring_soon,
            'total_classes': total_classes,
            'todays_bookings': todays_bookings,
        })


class RecentActivityView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        from members.models import Member
        from memberships.models import MemberMembership
        from classes.models import ClassBooking
        from django.db.models import Q

        user = request.user

        # Check if user is admin
        if user.role == 'admin' or user.is_staff:
            # Admin sees all activity
            recent_members = Member.objects.filter(
                is_active=True
            ).order_by('-created_at')[:5]
            
            recent_subscriptions = MemberMembership.objects.filter(
                Q(status='active') | Q(status='cancelled')
            ).order_by('-created_at')[:5]
            
            recent_bookings = ClassBooking.objects.filter(
                status='confirmed'
            ).order_by('-created_at')[:5]
        else:
            # Regular users see no activity
            recent_members = Member.objects.none()
            recent_subscriptions = MemberMembership.objects.none()
            recent_bookings = ClassBooking.objects.none()

        activities = []
        
        # Add recent members
        for member in recent_members:
            activities.append({
                'type': 'new_member',
                'title': f'New member: {member.full_name}',
                'description': f'Joined on {member.joined_date}',
                'timestamp': member.created_at,
                'icon': 'user'
            })
        
        # Add recent subscriptions
        for sub in recent_subscriptions:
            activities.append({
                'type': 'subscription',
                'title': f'{sub.member.full_name} subscribed to {sub.membership.name}',
                'description': f'Started: {sub.start_date}',
                'timestamp': sub.created_at,
                'icon': 'credit_card'
            })
        
        # Add recent bookings
        for booking in recent_bookings:
            activities.append({
                'type': 'booking',
                'title': f'{booking.member.full_name} booked {booking.gym_class.name}',
                'description': f'Class on {booking.booking_date}',
                'timestamp': booking.created_at,
                'icon': 'calendar'
            })
        
        # Sort all activities by timestamp
        activities.sort(key=lambda x: x['timestamp'], reverse=True)
        
        return Response(activities[:10])  # Return latest 10 activities


class LoadMockDataView(APIView):
    """
    Temporary endpoint to load mock data (remove in production)
    """
    def post(self, request):
        try:
            from members.management.commands.setup_mock_data import Command
            cmd = Command()
            cmd.handle()
            return Response({
                'message': 'Mock data loaded successfully!',
                'details': 'Created members, memberships, classes, and bookings'
            })
        except Exception as e:
            return Response({
                'error': f'Failed to load mock data: {str(e)}'
            }, status=500)


class PasswordResetRequestView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']

        try:
            user = User.objects.get(email=email)
            token = PasswordResetToken.objects.create(user=user)
            send_password_reset_email(email, token.token)
        except User.DoesNotExist:
            pass

        return Response({'message': 'If an account exists, a reset email has been sent'})


class PasswordResetConfirmView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            token = PasswordResetToken.objects.get(token=serializer.validated_data['token'])
            if not token.is_valid:
                return Response({'error': 'Token expired or already used'}, status=status.HTTP_400_BAD_REQUEST)

            user = token.user
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            token.used = True
            token.save()

            return Response({'message': 'Password reset successful'})
        except PasswordResetToken.DoesNotExist:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)
