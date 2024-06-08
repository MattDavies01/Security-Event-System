from .models import SecurityEvent, db
from sqlalchemy import func
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

# email settings
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_password'
ALERT_EMAIL = 'alert_recipient@example.com'

def analyze_events():
    """
    Analyze events to detect potential security issues.
    """
    now = datetime.utcnow()
    one_hour_ago = now - timedelta(hours=1)
    
    # Count failed login attempts in the last hour
    failed_logins_count = db.session.query(func.count(SecurityEvent.id)).filter(
        SecurityEvent.event_type == 'failed_login',
        SecurityEvent.timestamp >= one_hour_ago
    ).scalar()
    
    # failed login attmpts thershold
    threshold = 4
    
    if failed_logins_count > threshold:
        alert_message = f"High number of failed login attempts detected: {failed_logins_count} in the last hour."
        send_alert(alert_message)
    
    return {
        'failed_logins_count': failed_logins_count,
        'alert': failed_logins_count > threshold
    }

def send_alert(message):
    """
    Send an alert via email.
    """
    msg = MIMEText(message)
    msg['Subject'] = 'Security Alert'
    msg['From'] = SMTP_USERNAME
    msg['To'] = ALERT_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.sendmail(SMTP_USERNAME, ALERT_EMAIL, msg.as_string())
        print("Alert sent successfully!")
    except Exception as e:
        print(f"Failed to send alert: {e}")

# Utility function to log a new security event
def log_event(event_type, description):
    new_event = SecurityEvent(event_type=event_type, description=description)
    db.session.add(new_event)
    db.session.commit()
    print(f"Event logged: {event_type} - {description}")

# Example usage
if __name__ == "__main__":
    # Manually log  failed login attempt for testing
    log_event('failed_login', 'Failed login attempt for user admin')

    
    analysis_results = analyze_events()
    print(analysis_results)
