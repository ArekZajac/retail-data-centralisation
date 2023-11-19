WITH OrderedSales AS (
    SELECT
        ddt.year,
        LEAD(TO_TIMESTAMP(ddt.year || '-' || ddt.month || '-' || ddt.day || ' ' || ddt.timestamp, 'YYYY-MM-DD HH24:MI:SS')) 
        OVER (PARTITION BY ddt.year ORDER BY TO_TIMESTAMP(ddt.year || '-' || ddt.month || '-' || ddt.day || ' ' || ddt.timestamp, 'YYYY-MM-DD HH24:MI:SS')) 
        - TO_TIMESTAMP(ddt.year || '-' || ddt.month || '-' || ddt.day || ' ' || ddt.timestamp, 'YYYY-MM-DD HH24:MI:SS') AS time_to_next_sale
    FROM
        orders_table ot
    INNER JOIN dim_date_times ddt ON ot.date_uuid = ddt.date_uuid
),
AverageTime AS (
    SELECT
        year::integer,
        AVG(time_to_next_sale) AS avg_time
    FROM OrderedSales
    GROUP BY year
)
SELECT
    year,
    EXTRACT(HOUR FROM avg_time) AS hours,
    EXTRACT(MINUTE FROM avg_time) AS minutes,
    EXTRACT(SECOND FROM avg_time) AS seconds,
    (EXTRACT(MILLISECOND FROM avg_time) % 1000)::int AS milliseconds
FROM AverageTime
ORDER BY hours DESC, minutes DESC, seconds DESC, milliseconds DESC;
