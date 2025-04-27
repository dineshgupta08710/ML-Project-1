import logging
import os
from datetime import datetime

# 1. Create log file name with timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# 2. Define logs directory path
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)

# 3. Create the logs directory if it doesn't exist
os.makedirs(logs_path, exist_ok=True)

# 4. Full path to the log file
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# 5. Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO # only log messages at INFO level or higher (INFO, WARNING, ERROR, etc.)
)