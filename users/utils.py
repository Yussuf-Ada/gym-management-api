import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail


def send_password_reset_email(email, reset_token):
    frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
    reset_link = f"{frontend_url}/reset-password?token={reset_token}"

    message = Mail(
        from_email=os.getenv('DEFAULT_FROM_EMAIL', 'noreply@gym.com'),
        to_emails=email,
        subject='Password Reset Request',
        html_content=f'''
            <h2>Password Reset</h2>
            <p>You requested a password reset for your Gym Management account.</p>
            <p>Click the link below to reset your password:</p>
            <p><a href="{reset_link}">Reset Password</a></p>
            <p>This link will expire in 1 hour.</p>
            <p>If you didn't request this, please ignore this email.</p>
        '''
    )

    try:
        sg = SendGridAPIClient(os.getenv('SENDGRID_API_KEY'))
        sg.send(message)
        return True
    except Exception:
        return False
