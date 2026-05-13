import subprocess
import time
import logging
from logging.handlers import RotatingFileHandler

# Configuration
SERVICES = ["nginx", "ssh"]
CHECK_INTERVAL = 10
MAX_RETRIES = 3

# Setup logging with rotation
logger = logging.getLogger()
handler = RotatingFileHandler(
    "service_monitor.log", maxBytes=5 * 1024 * 1024, backupCount=3
)
formatter = logging.Formatter("[%(asctime)s] [%(levelname)s] %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Failure tracking
failure_count = {}

# Check service status with timeout
def is_service_running(service):
    try:
        result = subprocess.run(
            ["systemctl", "is-active", "--quiet", service],
            timeout=5
        )
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        logger.error(f"{service} check timed out")
        return False

# Restart service
def restart_service(service):
    subprocess.run(["systemctl", "restart", service])
    logger.warning(f"{service} restarted")

# Main monitoring loop
def monitor_services():
    logger.info("Starting service monitoring...")

    while True:
        for service in SERVICES:

            # Retry logic
            for attempt in range(MAX_RETRIES):
                if is_service_running(service):
                    logger.info(f"{service} is running ✅")
                    failure_count[service] = 0
                    break
                time.sleep(2)
            else:
                # Failure handling
                failure_count[service] = failure_count.get(service, 0) + 1
                logger.error(f"{service} is DOWN ❌")

                restart_service(service)

        time.sleep(CHECK_INTERVAL)

# ✅ Entry point
if __name__ == "__main__":
    monitor_services()
``
