import os
import smtplib
from dotenv import load_dotenv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# email credentials
load_dotenv()
EMAIL_SENDER_ALIAS = os.getenv("EMAIL_SENDER_ALIAS")
EMAIL_SENDER_PASSWORD = os.getenv("EMAIL_SENDER_PASSWORD")

# email server settings
smtp_server = "smtp.gmail.com"
smtp_port = 587


# send email with bus tracker updates
def send_email(receiver_email, linha, ponto, onibus_data):
    msg = MIMEMultipart()
    msg["From"] = str(EMAIL_SENDER_ALIAS)
    msg["To"] = receiver_email
    msg["Subject"] = "Bus Tracker Updates"

    # email body
    body = f"LINE: {linha}\nSTOP: {ponto}\n\n\n"
    for onibus, minutos in onibus_data.items():
        body += f"BUS: The bus {onibus} is {minutos} minutes away from the selected stop\n\n"

    msg.attach(MIMEText(body, "plain"))

    try:
        # connect email server and send email
        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(str(EMAIL_SENDER_ALIAS), str(EMAIL_SENDER_PASSWORD))
            server.send_message(msg)
            print(f"Email sent to {receiver_email}")
    except Exception as e:
        print(f"Error: {e}")
