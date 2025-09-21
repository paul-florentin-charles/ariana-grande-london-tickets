import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from twilio.rest import Client
from dotenv import load_dotenv

load_dotenv()

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_PHONE_NUMBER = os.getenv("TWILIO_PHONE_NUMBER")
RECIPIENT_PHONE_NUMBER = os.getenv("RECIPIENT_PHONE_NUMBER")

def send_notification(ticketmaster_url=None, axs_url=None):
    """
    Sends notifications if tickets are available.

    Args:
        ticketmaster_url (str, optional): URL for available Ticketmaster tickets. Defaults to None.
        axs_url (str, optional): URL for available AXS tickets. Defaults to None.
    """
    if not ticketmaster_url and not axs_url:
        print("No tickets available on any platform.")
        return

    subject = "Ariana Grande London Tickets Available!"
    body = "Tickets for Ariana Grande in London might be available!\n\n"

    if ticketmaster_url:
        body += f"Ticketmaster: {ticketmaster_url}\n"
    if axs_url:
        body += f"AXS: {axs_url}\n"

    #send_email(subject, body)
    send_whatsapp(body)

def send_email(subject, body):
    """
    Sends an email notification.

    Args:
        subject (str): The subject of the email.
        body (str): The body of the email.
    """
    # Email Configuration
    EMAIL_HOST = os.getenv("EMAIL_HOST")
    EMAIL_PORT = int(os.getenv("EMAIL_PORT"))
    EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
    EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
    RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

    if not all([EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_EMAIL]):
        print("Email credentials not configured. Skipping email notification.")
        return

    print(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD, RECIPIENT_EMAIL)

    try:
        message = MIMEMultipart()
        message["From"] = EMAIL_HOST_USER
        message["To"] = RECIPIENT_EMAIL
        message["Subject"] = subject
        message.attach(MIMEText(body, "plain"))

        with smtplib.SMTP(EMAIL_HOST, EMAIL_PORT) as server:
            server.starttls()
            server.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
            server.send_message(message)
            print("Email notification sent successfully.")

    except Exception as e:
        print(f"Failed to send email: {e}")

def send_whatsapp(body):
    """
    Sends a WhatsApp notification using Twilio.

    Args:
        body (str): The message to send.
    """
    if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_PHONE_NUMBER, RECIPIENT_PHONE_NUMBER]):
        print("Twilio credentials not configured. Skipping WhatsApp notification.")
        return

    try:
        client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)
        message = client.messages.create(
            body=body,
            from_=f"whatsapp:{TWILIO_PHONE_NUMBER}",
            to=f"whatsapp:{RECIPIENT_PHONE_NUMBER}"
        )
        print(RECIPIENT_PHONE_NUMBER, message, sep=": ")
        print(f"WhatsApp notification sent successfully to {message.sid}")

    except Exception as e:
        print(f"Failed to send WhatsApp message: {e}")
