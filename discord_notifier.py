import requests


WEBHOOK_URL = "https://discordapp.com/api/webhooks/1529463495156961441/k939IUGaDGWbQqCqJULLyOuDYIDOFNAm-fdVtHTKSdQk8SVrok3xBGrXGlkDMCLXm1GR"

def send_discord(message: str):
    if len(message) >= 2000:
        message = message[:1980] + "\n\n[TRUNCATED]"

    data = {
        "content": message,
        "username": "News Clanker 101"
    }

    response = requests.post(WEBHOOK_URL, json=data)

    if response.status_code == 204:
        print("Message sent successfully!")
    else:
        # Displays the error that occurred
        print("Something went wrong:", response.status_code)
        print(response.text)

