import json
import time
import sys
import os

from src import scanner
from src import notifier
from src import logger

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def start_watcher():
    config = load_config()
    logger.setup_logger(config['log_directory']) # One-time setup
    
    # Establish baseline
    active_port_data = {p['port']: p for p in scanner.get_listening_ports()}
    logging_ports = set(active_port_data.keys())
    
    notifier.logging.info(f"Watcher started. Monitoring ports. Whitelist: {config['authorized_ports']}")

    try:
        while True:
            time.sleep(config['scan_interval_seconds'])
            current_data = {p['port']: p for p in scanner.get_listening_ports()}
            current_ports = set(current_data.keys())

            # Detect New
            new_ports = current_ports - logging_ports
            for port in new_ports:
                is_auth = port in config['authorized_ports']
                notifier.alert_new_port(current_data[port], is_auth)

            # Detect Closed
            closed_ports = logging_ports - current_ports
            for port in closed_ports:
                notifier.logging.info(f"Port {port} has been closed.")

            logging_ports = current_ports
    except KeyboardInterrupt:
        notifier.logging.info("Shutting down tracker.")

if __name__ == "__main__":
    start_watcher()