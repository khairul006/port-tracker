import json
import time
import logging
import os
from dotenv import load_dotenv

load_dotenv()

from src import scanner
from src import alerts
from src.auditor import NetworkAuditor
from src.notifier import TelegramNotifier
from src.database import PortDatabase
from src.logger import setup_logger

def load_config():
    try:
        with open('config.json', 'r') as f:
            config = json.load(f)
    except FileNotFoundError:
        # Fallback if config.json is missing
        config = {}

    # Use .get() to avoid KeyErrors if 'telegram' section is missing in JSON
    tg_section = config.get('telegram', {})
    
    # Inject secrets directly into the dictionary
    tg_section['token'] = os.getenv('TELEGRAM_TOKEN')
    tg_section['chat_id'] = os.getenv('TELEGRAM_CHAT_ID')
    
    # Put it back in case it was missing
    config['telegram'] = tg_section
    return config

def start_watcher():
    config = load_config()
    # This sets up the 'PortTracker' logger in Python's memory
    setup_logger(config)
    # Grab the instance of that logger to use here in main.py
    logger = logging.getLogger("PortTracker")

    # Initialize the database
    db = PortDatabase() 

    # Initialize the class (the "Service")
    auditor_service = NetworkAuditor()

    # Initialize Telegram Service
    tg_config = config.get('telegram', {})
    notifier = TelegramNotifier(
        token=tg_config.get('token'), # Safe access
        chat_id=tg_config.get('chat_id'), 
        enabled=tg_config.get('enabled', False)
    )
    
    # Establish baseline
    active_port_data = {p['port']: p for p in scanner.get_listening_ports()}
    logging_ports = set(active_port_data.keys())
    
    logger.info(f"Watcher started. Monitoring ports. Whitelist: {config['authorized_ports']}")

    try:
        while True:
            time.sleep(config['scan_interval_seconds'])
            current_data = {p['port']: p for p in scanner.get_listening_ports()}
            current_ports = set(current_data.keys())

            # Detect New
            new_ports = current_ports - logging_ports
            for port in new_ports:
                # 1. Standard Alert
                is_auth = port in config['authorized_ports']
                db.log_port_event(port, "Open", is_auth) # save to database
                alerts.alert_new_port(current_data[port], is_auth)
                # 2. Trigger External Audit (Nmap)
                # We scan '127.0.0.1' for local, but in production, you might scan the Public IP
                audit_report = auditor_service.scan_port('127.0.0.1', port)
                alerts.notify(audit_report, "info")

                # 3. Send Telegram Alert
                alert_text = f"🚨 <b>New Port Detected!</b>\n\n{audit_report}"
                notifier.send_message(alert_text)

            # Detect Closed
            closed_ports = logging_ports - current_ports
            for port in closed_ports:
                db.log_port_event(port, "Closed")
                logger.info(f"Port {port} has been closed.")

            logging_ports = current_ports
    except KeyboardInterrupt:
        logger.info("Shutting down tracker.")

if __name__ == "__main__":
    start_watcher()