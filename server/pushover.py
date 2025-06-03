import os
import requests

api_user = os.getenv('PUSHOVER_API_USER')
if not api_user or not isinstance(api_user, str):
    raise ValueError('PUSHOVER_API_USER environment variable must be set.')

api_token = os.getenv("PUSHOVER_API_TOKEN")
if not api_token or not isinstance(api_token, str):
    raise ValueError('PUSHOVER_API_TOKEN evironment variable must be set.')

def send_alert(message: str) -> None:
    response = requests.post(
        "https://api.pushover.net/1/messages.json",
        data={
            "token": api_token,
            "user": api_user,
            "message": message,
        }
    )
    response.raise_for_status()
