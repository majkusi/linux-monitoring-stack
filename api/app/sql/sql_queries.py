

def avg_per_hour(metrics):
    list_of_metrics=""
    for metric in metrics:
        list_of_metrics += (f",avg({metric.upper()}) AS avg_{metric.lower()} " )

    return ("SELECT TO_CHAR(trunc(TIME_STAMP, 'HH24'), 'YYYY-MM-DD HH24:MI') AS hour "\
            + list_of_metrics +
            "FROM METRICS "\
            "GROUP BY trunc(TIME_STAMP, 'HH24')"\
            "ORDER BY trunc(TIME_STAMP, 'HH24');")
