import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

class TitanMail:
    def __init__(self):
        self.email = "your_email@gmail.com"  # Your address
        self.password = os.environ.get("MAIL_APP_PASSWORD") # Your App Password
        self.server = "smtp.gmail.com"
        self.port = 587

    def send(self, to_email, subject, body):
        try:
            msg = MIMEMultipart()
            msg['From'] = self.email
            msg['To'] = to_email
            msg['Subject'] = subject
            msg.attach(MIMEText(body, 'plain'))

            server = smtplib.SMTP(self.server, self.port)
            server.starttls() # Secure the connection
            server.login(self.email, self.password)
            server.send_message(msg)
            server.quit()
            return "Email sent successfully."
        except Exception as e:
            return f"Mail Error: {e}"

