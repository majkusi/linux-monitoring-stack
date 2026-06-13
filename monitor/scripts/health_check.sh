#!/bin/bash
while true; do
    ram_used=$(free -m | awk 'NR==2{print $3}')
    ram_total=$(free -m | awk 'NR==2{print $2}')
    ram_percentage=$(awk "BEGIN {printf \"%.2f\", ($ram_used/$ram_total)*100}")
    disk_used=$(df -h / | awk 'NR==2{print $5}')
    timestamp=$(date +"%Y-%m-%d %H:%M:%S")
    cpu_usage=$(top -bn1 | grep "Cpu(s)" | awk '{print $2 + $4}')
    cpu_percentage=$(awk "BEGIN {printf \"%.2f\", $cpu_usage}")
    echo "$timestamp,$ram_percentage,$ram_used,$ram_total,$disk_used,$cpu_percentage" >> /logs/health.log
    status=$(curl -s -o /dev/null -w "%{http_code}" http://tomcat:8080/)
    echo "$timestamp,$status" >> /logs/service.log
    sleep 60
done