import base64
from email.mime.text import MIMEText

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

from .config import get_settings

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def _get_credentials() -> Credentials:
    settings = get_settings()
    creds = Credentials.from_authorized_user_file(settings.gmail_token_path, SCOPES)

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())

    return creds


def send_gmail(to: str, subject: str, body: str) -> str:
    try:
        creds = _get_credentials()
    except FileNotFoundError:
        return (
            "No encontré el token de Gmail. Corre "
            "'python scripts/gmail_auth.py' siguiendo el apéndice de "
            "credenciales antes de usar esta herramienta."
        )

    service = build("gmail", "v1", credentials=creds)

    message = MIMEText(body)
    message["to"] = to
    message["subject"] = subject
    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()

    service.users().messages().send(userId="me", body={"raw": raw}).execute()
    return f"Correo enviado a {to} con asunto '{subject}'."
