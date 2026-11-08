"""Corre esto UNA SOLA VEZ para generar credentials/gmail_token.json.

Abre el navegador, pide iniciar sesión con la cuenta Gmail que va a enviar
los correos y aceptar el permiso de envío. Requiere que ya exista
credentials/gmail_client_secret.json (ver tutorial/apendice-credenciales.md).
"""

from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def main():
    flow = InstalledAppFlow.from_client_secrets_file(
        "credentials/gmail_client_secret.json", SCOPES
    )
    creds = flow.run_local_server(port=0)

    with open("credentials/gmail_token.json", "w") as f:
        f.write(creds.to_json())

    print("Listo: credentials/gmail_token.json generado.")


if __name__ == "__main__":
    main()
