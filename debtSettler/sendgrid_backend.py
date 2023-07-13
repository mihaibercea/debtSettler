# sendgrid_backend.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from django.core.mail.backends.base import BaseEmailBackend


class SendgridBackend(BaseEmailBackend):
    def send_messages(self, email_messages):
        sendgrid_client = SendGridAPIClient(api_key=self._get_sendgrid_api_key())
        for message in email_messages:
            mail = Mail(
                from_email=message.from_email,
                to_emails=message.to,
                subject=message.subject,
                plain_text_content=message.body
            )
            response = sendgrid_client.send(mail)
            if response.status_code != 202:
                raise Exception(f"Failed to send email: {response.body}")
