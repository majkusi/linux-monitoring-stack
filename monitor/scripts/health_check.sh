#!/bin/bash

#THRESHOLDS
DISK_THRESHOLD=80
RAM_THRESHOLD=85.00
CPU_THRESHOLD=90.00

while true; do
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    date_stamp=$(date +"%Y-%m-%d")

    #RAM
    ram_used=$(free -m | awk 'NR==2{print $3}')
    ram_total=$(free -m | awk 'NR==2{print $2}')
    ram_percentage=$(awk "BEGIN {printf \"%.2f\", ($ram_used/$ram_total)*100}")
    if awk -v ram_pr="$ram_percentage" -v ram_th="$RAM_THRESHOLD" 'BEGIN{exit ram_pr<ram_th}'; then
        echo "$timestamp, RAM ALERT: ${ram_percentage}% >= ${RAM_THRESHOLD}%" >> /logs/alerts-${date_stamp}.log
    fi

    #DISK
    disk_used=$(df -h / | awk 'NR==2{print $5}')
    disk_value=$(echo "$disk_used" | tr -d '%')
    if [ "$disk_value" -gt "$DISK_THRESHOLD" ]; then
        echo "$timestamp,DISK ALERT: ${disk_value}% > ${DISK_THRESHOLD}%" >> /logs/alerts-${date_stamp}.log
    fi
    
    #CPU
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
    cpu_percentage=$(awk "BEGIN {printf \"%.2f\", $cpu_usage}")
    if awk -v cpu_pr="$cpu_percentage" -v cpu_th="$CPU_THRESHOLD" 'BEGIN{exit cpu_pr<cpu_th}'; then 
        echo "$timestamp,CPU ALERT: ${cpu_percentage}% > ${CPU_THRESHOLD}%" >> /logs/alerts-${date_stamp}.log
    fi

    #LOGGING INTO FILE
    echo "$timestamp,$ram_percentage,$ram_used,$ram_total,$disk_used,$cpu_percentage" >> /logs/health-${date_stamp}.log
    status=$(curl -s -o /dev/null -w "%{http_code}" http://tomcat:8080/)
    echo "$timestamp,$status" >> /logs/service-${date_stamp}.log
    sleep 60
done