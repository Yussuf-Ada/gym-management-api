from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView
from .views import RegisterView, LoginView, LogoutView, UserProfileView, ChangePasswordView, DashboardStatsView, PasswordResetRequestView, PasswordResetConfirmView, RecentActivityView #, LoadMockDataView

urlpatterns = [
    path('auth/register/', RegisterView.as_view(), name='register'),
    path('auth/login/', LoginView.as_view(), name='login'),
    path('auth/logout/', LogoutView.as_view(), name='logout'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('auth/password-reset/', PasswordResetRequestView.as_view(), name='password_reset_request'),
    path('auth/password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('users/me/', UserProfileView.as_view(), name='user_profile'),
    path('users/me/change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('dashboard/stats/', DashboardStatsView.as_view(), name='dashboard_stats'),
    path('dashboard/activity/', RecentActivityView.as_view(), name='recent_activity'),
    # path('load-mock-data/', LoadMockDataView.as_view(), name='load_mock_data'),
]
