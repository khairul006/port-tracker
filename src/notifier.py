import logging

def setup_logging(log_file):
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[logging.FileHandler(log_file), logging.StreamHandler()]
    )

def alert_new_port(port_info, is_authorized):
    prefix = "[AUTHORIZED]" if is_authorized else "[!!! UNKNOWN !!!]"
    msg = f"{prefix} Port {port_info['port']} opened by {port_info['process']} (PID: {port_info['pid']})"
    
    if is_authorized:
        logging.info(msg)
    else:
        logging.warning(msg)