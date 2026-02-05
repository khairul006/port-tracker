import logging
import os
import sys
from datetime import datetime
from logging.handlers import RotatingFileHandler

def setup_logger(config):
    # Get the 'logging' object from config, or an empty dict if it's missing
    log_cfg = config.get('logging', {})

    # Read nested values with safe defaults
    log_dir = log_cfg.get('log_directory', 'storage/logs')
    max_bytes = log_cfg.get('max_bytes', 5242880)
    backup_count = log_cfg.get('backup_count', 5)

    # Ensure directory exists
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    # Generate filename with today's date: log-20260203.log
    today_str = datetime.now().strftime('%Y%m%d')
    log_filename = f"log-{today_str}.log"
    log_path = os.path.join(log_dir, log_filename)
    
    # Create the Formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    try:
        # RotatingFileHandler handles the suffixing logic.
        # By default, it adds .1, .2. 
        file_handler = RotatingFileHandler(
            log_path, 
            maxBytes=max_bytes, 
            backupCount=backup_count, 
            encoding='utf-8'
        )
        file_handler.setFormatter(formatter)
        
        # By default Python uses .1, .2. But we use our own format -1, -2,
        # we can change the namer function of the handler.
        file_handler.namer = lambda name: name.replace(".log.", "-") + (".log" if ".log" not in name.split("-")[-1] else "")
        
    except Exception as e:
        print(f"Error: Could not start file logger: {e}")
        file_handler = None

    # Setup Stream Handler (The Terminal/Console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # Get the Logger and attach handlers
    logger = logging.getLogger("PortTracker")
    logger.setLevel(logging.INFO)
    logger.propagate = False
    
    # Clean up any existing handlers to avoid double-logging
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.addHandler(stream_handler)
    if file_handler:
        logger.addHandler(file_handler)

    return logger