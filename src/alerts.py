import logging

# Define this once at the top of your file
logger = logging.getLogger("PortTracker")

def notify(message, level="info"):
    if level == "warning":
        logger.warning(f"🚨 ALERT: {message}")
    elif level == "error":
        logger.error(f"❌ ERROR: {message}")
    else:
        logger.info(message)

def alert_new_port(port_info, is_authorized):
    prefix = "[AUTHORIZED]" if is_authorized else "[!!! UNKNOWN !!!]"
    msg = f"{prefix} Port {port_info['port']} opened by {port_info['process']} (PID: {port_info['pid']})"
    
    if is_authorized:
        logger.info(msg)
    else:
        logger.warning(msg)

