#!/bin/bash
/scripts/health_check.sh &

while true; do 
    /scripts/log_cleanup.sh
    sleep 86400
done