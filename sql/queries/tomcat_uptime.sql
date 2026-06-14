SELECT successes, total, ROUND(successes/total * 100, 2) AS uptime_pct
FROM(SELECT SUM(
    CASE WHEN HTTP_STATUS = 200 THEN 1 ELSE 0 END) AS successes,
    COUNT(*) AS total  
FROM STATUS);
