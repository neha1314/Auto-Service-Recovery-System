#!/bin/bash

# Configuration
SERVICES=("nginx" "ssh")
INTERVAL=10
RETRIES=3

# Log file
LOGFILE="service_monitor.log"

echo "$(date): Starting service monitoring" >> "$LOGFILE"

while true; do
  for SERVICE in "${SERVICES[@]}"; do

    count=0
    running=false

    #  Retry logic
    while [ $count -lt $RETRIES ]; do
      if systemctl is-active --quiet "$SERVICE"; then
        echo "$(date): $SERVICE is running " >> "$LOGFILE"
        running=true
        break
      fi
      ((count++))
      sleep 2
    done

    # If still not running → restart
    if [ "$running" = false ]; then
      echo "$(date): $SERVICE is DOWN , restarting..." >> "$LOGFILE"
      systemctl restart "$SERVICE"
      echo "$(date): $SERVICE restarted" >> "$LOGFILE"
    fi

  done

  sleep $INTERVAL
done
