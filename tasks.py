from celery import Celery
from datetime import datetime
from email.mime.text import MIMEText
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

# Initialize a Celery application
app = Celery('tasks')
app.config_from_object('celery_config')

# Define a Celery task to send an email
@app.task
def send_email(to_email):
    smtp_server = "smtp.gmail.com"
    smtp_port = 465
    from_email = os.getenv("SMTP_EMAIL")
    from_password = os.getenv("SMTP_PASSWORD")
    subject = "Test Email"
    body = "Hallo there, This is a test email."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = from_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP_SSL(smtp_server, smtp_port)
        server.set_debuglevel(1)
        server.login(from_email, from_password)
        server.sendmail(from_email, to_email, msg.as_string())
        server.quit()
        return f"Email sent to {to_email}"
    except Exception as e:
        return str(e)

# Define a Celery task to log the current time
@app.task
def log_current_time():
    log_file_path = '/var/log/messaging_system.log'

    try:
        os.makedirs(os.path.dirname(log_file_path), exist_ok=True)
        if not os.path.isfile(log_file_path):
            with open(log_file_path, 'w'):
                pass
            os.chmod(log_file_path, 0o664)

        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with open(log_file_path, 'a') as log_file:
            log_file.write(f"{current_time}\n")
        return f"Logged time: {current_time}"
    except Exception as e:
        return str(e)
