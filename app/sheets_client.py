from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

from .config import get_settings

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def append_row(spreadsheet_id: str, valores: list[str]) -> str:
    settings = get_settings()

    try:
        creds = Credentials.from_service_account_file(
            settings.google_service_account_path, scopes=SCOPES
        )
    except FileNotFoundError:
        return (
            "No encontré credentials/google_service_account.json. Sigue el "
            "apéndice de credenciales antes de usar esta herramienta."
        )

    service = build("sheets", "v4", credentials=creds)
    service.spreadsheets().values().append(
        spreadsheetId=spreadsheet_id,
        range="A1",
        valueInputOption="USER_ENTERED",
        insertDataOption="INSERT_ROWS",
        body={"values": [valores]},
    ).execute()

    return f"Fila agregada a la hoja: {valores}"
