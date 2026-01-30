import logging
import os
import sys
from datetime import datetime

def setup_logger(log_dir):
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)

    log_path = os.path.join(log_dir, f"log-{datetime.now().strftime('%Y%m%d')}.log")
    
    # 1. Create the Formatter
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(name)s: %(message)s')

    # 2. Setup File Handler (Crucial: encoding='utf-8')
    file_handler = logging.FileHandler(log_path, encoding='utf-8')
    file_handler.setFormatter(formatter)

    # 3. Setup Stream Handler (The Terminal/Console)
    stream_handler = logging.StreamHandler(sys.stdout)
    stream_handler.setFormatter(formatter)

    # 4. Get the Logger and attach handlers
    logger = logging.getLogger("PortTracker")
    logger.setLevel(logging.INFO)
    
    # Clean up any existing handlers to avoid double-logging
    if logger.hasHandlers():
        logger.handlers.clear()
        
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    
    # Pro Tip: Also fix the root logger just in case other libraries log things
    logging.getLogger().handlers = [stream_handler, file_handler]
    logging.getLogger().setLevel(logging.INFO)

    return logger