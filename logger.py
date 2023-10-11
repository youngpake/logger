import logging
import requests
import random


class CustomLogger:
    """
    Custom logging class that provides multiple levels of logging:
    - info_log: Logs informational messages.
    - critical_log_to_file: Logs critical messages to a file.
    - critical_log_to_pushover: Sends critical messages to Pushover and logs them.
    - daily_check_log: Checks daily tasks and logs the outcome.
    - send_pushover_message: Sends a message via Pushover.
    """

    def __init__(self, po_api_key, po_user_key):
        self.po_api_key = po_api_key
        self.po_user_key = po_user_key
        logging.basicConfig(filename='application.log', level=logging.INFO)
        self.logger = logging.getLogger()
    
    def info_log(self, message):
        """Logs informational messages."""
        self.logger.info(message)

    def critical_log_to_file(self, message):
        """Logs critical messages to the file."""
        self.info_log(message)
        self.logger.critical(message)

    def critical_log_to_pushover(self, message):
        """Logs critical messages and sends them to Pushover."""
        self.critical_log_to_file(message)
        self.send_pushover_message("Critical Alert", message, -1)

    def doomsday_logger(self, message):
        """Let's hope this never executes, but you know what this is for."""
        stoic_titles = [
            "Titanic Sunk, Details Inside.",
            "Armageddon Alert, Proceed Calmly.",
            "Universe Imploding, Read Log.",
            "End of Days, See Details.",
            "Chaos Reigns, Consult Log.",
            "Cataclysm Confirmed, Debug Now.",
            "Doom Descends, Check Log.",
            "Existential Crisis, Review Alert.",
            "Final Countdown, Debug Awaits.",
            "Ragnarok Initiated, Log Updated."
        ]
        chosen_title = random.choice(stoic_titles)
        self.send_pushover_message(chosen_title, message, 2)

    def daily_check_log(self, check_passed, message):
        """Logs the outcome of daily checks to application and pushover"""
        if check_passed:
            self.info_log(f"Daily check passed: {message}")
        else:
            self.critical_log_to_pushover(f"Daily check failed: {message}")

    def send_pushover_message(self, title, message, priority=0):
        """
        Sends a message via Pushover with a specified priority level.

        :param str token: API token for Pushover
        :param str user: User key for the recipient
        :param str message: Message content to send
        :param int priority: Priority level of the message. The levels are as follows:
        
        - -2: Silently deliver to notification shade, no sound.
        - -1: Generate a notification, but no sound.
        - 0: (default) Generate a notification with default sound.
        - 1: High-priority, bypasses quiet hours.
        - 2: High-priority, continues alerting until acknowledged by the user.

        :return: True if the request was successful, otherwise False
        :rtype: bool
        """
        payload = {
            "token": self.po_api_key,
            "user": self.po_user_key,
            "title": title,
            "message": message,
            "priority": priority
        }
        r = requests.post("https://api.pushover.net/1/messages.json", data=payload)
        return r.status_code == 200
