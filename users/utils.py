import os
from django.core.mail import send_mail


def send_password_reset_email(email, reset_token):
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    reset_link = f"{frontend_url}/reset-password?token={reset_token}"

    subject = 'Password Reset Request'
    message = f'''
        Password Reset
        
        You requested a password reset for your Gym Management account.
        
        Click the link below to reset your password:
        {reset_link}
        
        This link will expire in 1 hour.
        
        If you didn't request this, please ignore this email.
    '''
    html_message = f'''
        <h2>Password Reset</h2>
        <p>You requested a password reset for your Gym Management account.</p>
        <p>Click the link below to reset your password:</p>
        <p><a href="{reset_link}">Reset Password</a></p>
        <p>This link will expire in 1 hour.</p>
        <p>If you didn't request this, please ignore this email.</p>
    '''

    try:
        send_mail(
            subject,
            message,
            os.getenv('DEFAULT_FROM_EMAIL', 'noreply@gym.com'),
            [email],
            html_message=html_message,
            fail_silently=False,
        )
        return True
    except Exception as e:
        print(f"Failed to send password reset email: {e}")
        return False
