from gen_api import summarise
from discord_notifier import send_discord
import logging
import sys


if __name__ == "__main__":
    message: str = summarise()
    partitioned = message.split('\n\n\n')

    for summary in partitioned:
        output = '\n\n\n' + summary + '\n\n\n'
        send_discord(output)

    # Logging the last run made
    logging.basicConfig(
        filename='run_log.txt', # log into a file with this name (creation or overriding),
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Redirecting all print statements directly into the log file
    sys.stdout = open(file='run_log.txt', mode='a') # standard print output
    sys.stderr = open(file='run_log.txt', mode='a') # error output

