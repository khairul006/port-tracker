import requests
import logging

logger = logging.getLogger("PortTracker")

class TelegramNotifier:
    def __init__(self, token, chat_id, enabled=True):
        self.token = token
        self.chat_id = chat_id
        self.enabled = enabled
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send_message(self, text):
        if not self.enabled:
            return

        payload = {
            "chat_id": self.chat_id,
            "text": text,
            "parse_mode": "HTML"
        }

        try:
            response = requests.post(self.base_url, data=payload)
            response.raise_for_status() # Raises an error if the status is 4xx or 5xx
            logger.info("Telegram notification sent successfully.")
        except Exception as e:
            logger.error(f"Failed to send Telegram alert: {e}")