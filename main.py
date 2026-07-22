from gen_api import summarise
from discord_notifier import send_discord


if __name__ == "__main__":
    message: str = summarise()
    partitioned = message.split('\n\n\n')

    for summary in partitioned:
        output = '\n\n\n' + summary + '\n\n\n'
        send_discord(output)

