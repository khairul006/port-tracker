import logging

logger = logging.getLogger("PortTracker")

def notify(message, level="info"):
    """
    This is the single entry point for all notifications.
    It currently logs, but later it can send Telegram/Email.
    """
    if level == "warning":
        logger.warning(f"🚨 ALERT: {message}")
    else:
        logger.info(message)

def alert_new_port(port_info, is_authorized):
    prefix = "[AUTHORIZED]" if is_authorized else "[!!! UNKNOWN !!!]"
    msg = f"{prefix} Port {port_info['port']} opened by {port_info['process']} (PID: {port_info['pid']})"
    
    if is_authorized:
        logging.info(msg)
    else:
        logging.warning(msg)

def send_telegram(message):
    # Future integration point
    pass