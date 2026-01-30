import json
import time
import sys
import os

from src import scanner
from src import alerts
from src import logger
from src.auditor import NetworkAuditor

def load_config():
    with open('config.json', 'r') as f:
        return json.load(f)

def start_watcher():
    config = load_config()
    logger.setup_logger(config['log_directory']) # One-time setup

    # Initialize the class (the "Service")
    auditor_service = NetworkAuditor()
    
    # Establish baseline
    active_port_data = {p['port']: p for p in scanner.get_listening_ports()}
    logging_ports = set(active_port_data.keys())
    
    alerts.logging.info(f"Watcher started. Monitoring ports. Whitelist: {config['authorized_ports']}")

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
                alerts.alert_new_port(current_data[port], is_auth)
                # 2. Trigger External Audit (Nmap)
                # We scan '127.0.0.1' for local, but in production, you might scan the Public IP
                audit_report = auditor_service.scan_port('127.0.0.1', port)
                alerts.notify(audit_report, "info")

            # Detect Closed
            closed_ports = logging_ports - current_ports
            for port in closed_ports:
                alerts.logging.info(f"Port {port} has been closed.")

            logging_ports = current_ports
    except KeyboardInterrupt:
        alerts.logging.info("Shutting down tracker.")

if __name__ == "__main__":
    start_watcher()