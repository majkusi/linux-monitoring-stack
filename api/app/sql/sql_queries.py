def avg_per_hour(metrics):
    str_of_metrics=""
    for metric in metrics:
        str_of_metrics += (f",avg({metric.upper()}) AS avg_{metric.lower()} " )

    return ("SELECT TO_CHAR(trunc(TIME_STAMP, 'HH24'), 'YYYY-MM-DD HH24:MI') AS hour "\
            + str_of_metrics +
            "FROM METRICS "\
            "GROUP BY trunc(TIME_STAMP, 'HH24')"\
            "ORDER BY trunc(TIME_STAMP, 'HH24')")

def count_http_errors_per_day():
    return ("SELECT trunc(TIME_STAMP, 'DD') AS day, "
            "COUNT(HTTP_STATUS) AS error_count "
            "FROM STATUS "
            "WHERE HTTP_STATUS != 200 "
            "GROUP BY trunc(TIME_STAMP, 'DD') "
            "ORDER BY trunc(TIME_STAMP, 'DD')")

def server_uptime_pct():
    return ("SELECT NVL(SUM(CASE WHEN HTTP_STATUS != 0 THEN 1 ELSE 0 END), 0) AS successes, "
            "COUNT(*) AS total, "
            "NVL(ROUND(SUM(CASE WHEN HTTP_STATUS != 0 THEN 1 ELSE 0 END) / NULLIF(COUNT(*), 0) * 100, 2), 0) AS uptime_pct "
            "FROM STATUS")
