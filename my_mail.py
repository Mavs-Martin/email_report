import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import schedule
import time
import os

def send_email_report():
    smtp_server = "smtp.gmail.com"
    port = 587  # For starttls
    sender_email = os.getenv("SENDER_EMAIL")
    password = os.getenv("EMAIL_PASSWORD")
    receiver_email = os.getenv("RECEIVER_EMAIL")

    subject = "Daily Report"
    body = "This is your daily report."

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    # Create secure connection with server and send email
    context = ssl.create_default_context()

    try:
        with smtplib.SMTP(smtp_server, port) as server:
            server.starttls(context=context)  # Secure the connection
            server.login(sender_email, password)
            server.sendmail(sender_email, receiver_email, message.as_string())
        print("Email sent successfully")
    except Exception as e:
        print(f"Error: {e}")

# Schedule the email to be sent daily at a specific time
schedule.every().day.at("08:00").do(send_email_report)

# Keep the script running
while True:
    schedule.run_pending()
    time.sleep(60)  # wait one minute
